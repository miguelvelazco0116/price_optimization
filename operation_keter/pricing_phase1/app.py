"""OPERATION KETER · Pricing Elasticity · Fase 1.1."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from elasticity import ElasticityInputError, analyze_price_elasticity


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
                analysis = analyze_price_elasticity(frame, price_column, volume_column)
            except ElasticityInputError as exc:
                st.error(str(exc))
            else:
                st.metric("Elasticidad precio", f"{analysis.elasticity:.4f}")
                if analysis.variance_status == "heteroscedastic":
                    st.warning("Se detectó evidencia de heterocedasticidad (Breusch–Pagan, p < 0.05).")
                elif analysis.variance_status == "not_rejected":
                    st.info(
                        "No se detectó evidencia suficiente de heterocedasticidad "
                        "(esto no confirma homocedasticidad)."
                    )
                else:
                    st.info("Prueba de Breusch–Pagan no evaluable: residuos casi nulos.")

                with st.expander("Detalle estadístico"):
                    if analysis.bp_pvalue is not None:
                        st.write(f"Breusch–Pagan · p-valor: {analysis.bp_pvalue:.4g}")
                    st.caption("H₀: varianza constante de los errores · α = 0.05")
                    if analysis.hc3_standard_error is not None:
                        st.write(f"Error estándar robusto HC3: {analysis.hc3_standard_error:.4f}")
                    if analysis.hc3_confidence_interval is not None:
                        low, high = analysis.hc3_confidence_interval
                        st.write(f"Intervalo de confianza robusto al 95%: [{low:.4f}, {high:.4f}]")
                    st.caption(
                        "HC3 corrige la incertidumbre estimada, no modifica la elasticidad OLS. "
                        "Esta regresión simple no demuestra causalidad."
                    )
