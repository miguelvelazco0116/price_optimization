"""Regresiones y validaciones del estimador de elasticidad."""

import numpy as np
import pandas as pd
import pytest

from elasticity import ElasticityInputError, estimate_price_elasticity


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
