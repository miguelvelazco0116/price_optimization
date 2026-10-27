"""Regresiones, diagnósticos Breusch–Pagan y validaciones."""

import numpy as np
import pandas as pd
import pytest
import statsmodels.api as sm

from elasticity import (
    ElasticityInputError,
    analyze_price_elasticity,
    estimate_price_elasticity,
)


def test_recovers_exact_loglog_elasticity():
    price = np.linspace(10, 30, 40)
    volume = 1_000 * price ** (-1.7)
    frame = pd.DataFrame({"precio": price, "volumen": volume})
    assert estimate_price_elasticity(frame, "precio", "volumen") == pytest.approx(-1.7, abs=1e-10)


@pytest.mark.parametrize(
    "price, volume",
    [
        ([10.0] * 8, [100, 90, 80, 70, 60, 50, 40, 30]),
        ([0, 11, 12, 13, 14, 15, 16, 17], [100] * 8),
        ([10, 11, 12, 13, 14, 15, 16, 17], [100, 90, 80, 70, 60, 50, 0, 30]),
        ([10, 11, 12, 13, 14, 15, 16, None], [100] * 8),
        ([10, 11, 12, 13, 14, 15, 16, 17], [100, 90, 80, 70, 60, 50, 40, "texto"]),
    ],
)
def test_rejects_invalid_records(price, volume):
    with pytest.raises(ElasticityInputError):
        estimate_price_elasticity(pd.DataFrame({"p": price, "q": volume}), "p", "q")


def test_rejects_small_sample():
    with pytest.raises(ElasticityInputError, match="8 observaciones"):
        estimate_price_elasticity(pd.DataFrame({"p": [1, 2, 3], "q": [6, 5, 4]}), "p", "q")


def test_rejects_duplicate_selected_columns():
    frame = pd.DataFrame({"p": range(1, 9), "q": range(8, 0, -1)})
    with pytest.raises(ElasticityInputError, match="diferentes"):
        estimate_price_elasticity(frame, "p", "p")


def test_rejects_missing_column():
    frame = pd.DataFrame({"p": range(1, 9), "q": range(8, 0, -1)})
    with pytest.raises(ElasticityInputError, match="No se encontraron"):
        estimate_price_elasticity(frame, "p", "other")


def _synthetic_data(heteroscedastic: bool) -> pd.DataFrame:
    rng = np.random.default_rng(21)
    log_price = np.linspace(1.5, 4.0, 180)
    if heteroscedastic:
        noise_sd = 0.025 + 0.30 * (log_price - log_price.min()) / np.ptp(log_price)
    else:
        noise_sd = np.full_like(log_price, 0.10)
    log_volume = 8.0 - 1.5 * log_price + rng.normal(size=len(log_price)) * noise_sd
    return pd.DataFrame({"price": np.exp(log_price), "volume": np.exp(log_volume)})


def test_detects_strong_heteroscedasticity():
    data = _synthetic_data(heteroscedastic=True)
    outcome = analyze_price_elasticity(data, "price", "volume")

    assert outcome.variance_status == "heteroscedastic"
    assert outcome.bp_pvalue is not None and outcome.bp_pvalue < 0.05
    assert outcome.hc3_standard_error is not None and outcome.hc3_standard_error > 0
    assert outcome.hc3_confidence_interval is not None


def test_no_evidence_of_heteroscedasticity_for_constant_variance():
    data = _synthetic_data(heteroscedastic=False)
    outcome = analyze_price_elasticity(data, "price", "volume")
    assert outcome.variance_status == "not_rejected"
    assert outcome.bp_pvalue is not None and outcome.bp_pvalue >= 0.05


def test_hc3_does_not_change_ols_slope():
    data = _synthetic_data(heteroscedastic=True)
    result = analyze_price_elasticity(data, "price", "volume")
    log_price = np.log(data["price"].to_numpy())
    log_volume = np.log(data["volume"].to_numpy())
    baseline_ols = sm.OLS(log_volume, sm.add_constant(log_price)).fit()
    assert result.elasticity == pytest.approx(float(baseline_ols.params[1]), abs=1e-12)
    assert result.elasticity == pytest.approx(estimate_price_elasticity(data, "price", "volume"))


def test_perfect_fit_does_not_fake_diagnostic():
    price = np.linspace(10.0, 40.0, 40)
    volume = 2000 * price ** (-1.3)
    outcome = analyze_price_elasticity(pd.DataFrame({"p": price, "q": volume}), "p", "q")
    assert outcome.elasticity == pytest.approx(-1.3)
    assert outcome.variance_status == "indeterminate"
    assert outcome.bp_pvalue is None


def test_invalid_significance_threshold():
    data = _synthetic_data(heteroscedastic=False)
    with pytest.raises(ValueError, match="nivel de significancia"):
        analyze_price_elasticity(data, "price", "volume", alpha=1.0)
