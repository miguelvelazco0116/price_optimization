# OPERATION KETER — Fase 1.1: Pricing Elasticity + Diagnóstico

Aplicación **Streamlit** para estimar elasticidad precio con una regresión **OLS log-log**, realizar una prueba de **heterocedasticidad** y reportar incertidumbre robusta.

## Alcance

1. Cargar archivo histórico `.csv` o `.xlsx` (primera hoja, máximo 10 MB).
2. Seleccionar las columnas de precio y volumen.
3. Pulsar **Calcular elasticidad**.
4. Ver un **único indicador principal: elasticidad precio**.
5. Ver diagnóstico breve de Breusch–Pagan; el detalle opcional muestra su p-valor, error estándar HC3 e intervalo de confianza.

No incorpora aún simulaciones, optimización, recomendaciones de precio ni proyecciones de profit.

## Modelo

`ln(volumen) = β₀ + β₁ × ln(precio) + error`

**Elasticidad precio = β₁**. Ejemplo: β₁ = -1.5 implica que un aumento del 1% en precio se asocia aproximadamente con una caída del 1.5% de volumen, manteniendo los supuestos del modelo.

### Diagnóstico de heterocedasticidad

- Prueba **Koenker–Breusch–Pagan** sobre los residuos del modelo, con regresores [constante, ln(precio)].
- Hipótesis nula H₀: varianza condicional constante (homocedasticidad).
- Nivel de significancia fijado en **α = 0.05**.
- Si `p < 0.05`, se muestra **«evidencia de heterocedasticidad»**.
- Si `p >= 0.05`, se muestra **«sin evidencia suficiente de heterocedasticidad»**; esto **no prueba** homocedasticidad.
- Si el ajuste es prácticamente perfecto, los residuos son insuficientes para evaluar la prueba y se informa **«no evaluable»**.
- Se calculan errores estándar e IC al 95% robustos **HC3** para la elasticidad; se muestran en el detalle opcional. HC3 **no cambia el coeficiente OLS**, solo su inferencia.

> Importante: la heterocedasticidad no es el único riesgo de una estimación. La endogeneidad de precio, promociones, estacionalidad, precios de competidores o autocorrelación pueden sesgar o invalidar inferencias. Este modelo bivariado describe asociación histórica; **no demuestra efecto causal del precio**. HC3 no corrige endogeneidad ni autocorrelación. Para series cronológicas será necesario evaluar esa dependencia en una fase posterior.

## Requisitos de datos

- Mínimo **8 observaciones** (es un mínimo técnico, no garantiza potencia estadística para Breusch–Pagan).
- Precio y volumen estrictamente **mayores que cero** en todas las filas.
- Valores numéricos sin símbolos monetarios ni valores vacíos.
- Precio con variación suficiente; se rechazan filas inválidas en vez de eliminarlas silenciosamente.
- Datos comparables de un producto y un mercado, con observaciones de periodos homogéneos.

Ejemplo sintético: [`data/example.csv`](data/example.csv).

## Ejecutar (Windows PowerShell)

Desde esta carpeta:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Abre la dirección local que indique Streamlit (normalmente `http://localhost:8501`).

## Pruebas

```powershell
python -m pip install pytest
python -m pytest -q
```

## Estructura

- `app.py`: interfaz de Streamlit.
- `elasticity.py`: estimador OLS log-log, Breusch–Pagan y HC3.
- `tests/test_elasticity.py`: pruebas de estimación y de condiciones de varianza.
- `data/example.csv`: dataset sintético para pruebas.

## Evolución futura

Diagnósticos de autocorrelación, controles por promociones y estacionalidad, estimación causal y motor de optimización comercial. Ninguno forma parte de esta fase.
