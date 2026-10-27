"""Estimación de elasticidad-precio con regresión OLS log-log."""

from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm


class ElasticityInputError(ValueError):
    """Señala que los datos no permiten estimar una elasticidad válida."""


def estimate_price_elasticity(
    data: pd.DataFrame,
    price_column: str,
    volume_column: str,
) -> float:
    """Devuelve el coeficiente de log(precio) en log(volumen) ~ log(precio).

    El modelo incluye intercepto. No elimina observaciones de manera silenciosa.
    La estimación describe una asociación histórica, no causalidad demostrada.
    """
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

    return elasticity
