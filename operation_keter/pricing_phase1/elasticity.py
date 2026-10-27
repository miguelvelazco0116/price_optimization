"""Elasticidad OLS log-log y diagnóstico de heterocedasticidad Breusch–Pagan."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.diagnostic import het_breuschpagan


class ElasticityInputError(ValueError):
    """Los datos no permiten estimar una elasticidad válida."""


@dataclass(frozen=True)
class ElasticityAnalysis:
    """Resultados del análisis, manteniendo el coeficiente como salida principal."""

    elasticity: float
    bp_pvalue: float | None
    variance_status: str  # "heteroscedastic", "not_rejected" o "indeterminate"
    hc3_standard_error: float | None
    hc3_confidence_interval: tuple[float, float] | None


def analyze_price_elasticity(
    data: pd.DataFrame,
    price_column: str,
    volume_column: str,
    alpha: float = 0.05,
) -> ElasticityAnalysis:
    """Estima OLS log-log y prueba H0: varianza de errores constante.

    La prueba Koenker–Breusch–Pagan usa log(precio) e intercepto.
    HC3 ajusta la inferencia (errores estándar e IC), no el coeficiente OLS.
    Los diagnósticos no identifican por sí mismos elasticidad causal.
    """
    if not (0.0 < alpha < 1.0):
        raise ValueError("El nivel de significancia debe estar entre 0 y 1.")

    if price_column == volume_column:
        raise ElasticityInputError("Precio y volumen deben usar columnas diferentes.")

    if price_column not in data.columns or volume_column not in data.columns:
        raise ElasticityInputError("No se encontraron las columnas seleccionadas.")

    if len(data) < 8:
        raise ElasticityInputError("Se requieren al menos 8 observaciones históricas.")

    price = pd.to_numeric(data[price_column], errors="coerce")
    volume = pd.to_numeric(data[volume_column], errors="coerce")

    if not np.isfinite(price.to_numpy(dtype=float)).all():
        raise ElasticityInputError("La columna de precio contiene valores vacíos o no numéricos.")
    if not np.isfinite(volume.to_numpy(dtype=float)).all():
        raise ElasticityInputError("La columna de volumen contiene valores vacíos o no numéricos.")
    if (price <= 0).any() or (volume <= 0).any():
        raise ElasticityInputError("Todos los precios y volúmenes deben ser mayores que cero.")
    if price.nunique() < 2:
        raise ElasticityInputError("El precio debe variar entre las observaciones.")

    log_price = np.log(price.to_numpy(dtype=float))
    log_volume = np.log(volume.to_numpy(dtype=float))

    if float(np.std(log_price)) < 1e-10:
        raise ElasticityInputError("La variación del precio es insuficiente para estimar elasticidad.")

    x = sm.add_constant(log_price, has_constant="add")
    result = sm.OLS(log_volume, x).fit()
    elasticity = float(result.params[1])

    if not np.isfinite(elasticity):
        raise ElasticityInputError("No fue posible obtener una elasticidad finita.")

    # Si el ajuste es casi exacto, no hay variación residual interpretable
    # sobre la que realizar una prueba válida de heterocedasticidad.
    bp_pvalue: float | None = None
    variance_status = "indeterminate"
    if float(np.max(np.abs(result.resid))) > 1e-10:
        _, raw_pvalue, _, _ = het_breuschpagan(result.resid, x, robust=True)
        if np.isfinite(raw_pvalue):
            bp_pvalue = float(raw_pvalue)
            variance_status = "heteroscedastic" if bp_pvalue < alpha else "not_rejected"

    robust = result.get_robustcov_results(cov_type="HC3")
    standard_error = float(robust.bse[1])
    ci = robust.conf_int(alpha=alpha)[1]
    hc3_standard_error = standard_error if np.isfinite(standard_error) else None
    hc3_confidence_interval = (
        (float(ci[0]), float(ci[1])) if np.isfinite(ci).all() else None
    )

    return ElasticityAnalysis(
        elasticity=elasticity,
        bp_pvalue=bp_pvalue,
        variance_status=variance_status,
        hc3_standard_error=hc3_standard_error,
        hc3_confidence_interval=hc3_confidence_interval,
    )


def estimate_price_elasticity(
    data: pd.DataFrame,
    price_column: str,
    volume_column: str,
) -> float:
    """API compatible con Fase 1: devuelve exclusivamente el coeficiente."""
    return analyze_price_elasticity(data, price_column, volume_column).elasticity
