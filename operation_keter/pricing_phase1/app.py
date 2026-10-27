"""OPERATION KETER · Pricing Elasticity · Fase 1."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from elasticity import ElasticityInputError, estimate_price_elasticity


st.set_page_config(
    page_title="KETER | Elasticidad precio",
    page_icon="🎯",
    layout="centered",
)

st.title("OPERATION KETER")
st.caption("FASE 1 · PRICING ELASTICITY · OLS LOG-LOG")
st.write("Carga tus datos históricos y selecciona las columnas de precio y volumen.")

uploaded = st.file_uploader("Archivo histórico (.csv o .xlsx)", type=["csv", "xlsx"])

if uploaded is not None:
    try:
        if uploaded.size > 10 * 1024 * 1024:
            raise ValueError("El archivo supera el límite de 10 MB.")

        if Path(uploaded.name).suffix.lower() == ".xlsx":
            frame = pd.read_excel(uploaded)
        else:
            frame = pd.read_csv(uploaded, sep=None, engine="python")

        if len(frame.columns) < 2:
            raise ValueError("El archivo debe contener al menos dos columnas.")
        if frame.empty:
            raise ValueError("El archivo no contiene observaciones.")

    except (ValueError, pd.errors.ParserError, ImportError, OSError) as exc:
        st.error(f"No fue posible leer el archivo: {exc}")
    else:
        columns = list(frame.columns)
        price_guess = next(
            (i for i, col in enumerate(columns) if "prec" in str(col).lower() or "price" in str(col).lower()),
            0,
        )
        price_column = st.selectbox("Columna de precio", columns, index=price_guess)
        volume_options = [col for col in columns if col != price_column]
        volume_guess = next(
            (
                i
                for i, col in enumerate(volume_options)
                if any(word in str(col).lower() for word in ("vol", "unid", "unit", "qty", "sales"))
            ),
            0,
        )
        volume_column = st.selectbox("Columna de volumen", volume_options, index=volume_guess)

        if st.button("Calcular elasticidad", type="primary", use_container_width=True):
            try:
                estimate = estimate_price_elasticity(frame, price_column, volume_column)
            except ElasticityInputError as exc:
                st.error(str(exc))
            else:
                st.metric("Elasticidad precio", f"{estimate:.4f}")
