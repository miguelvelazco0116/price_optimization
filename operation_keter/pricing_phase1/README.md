# OPERATION KETER — Fase 1: Pricing Elasticity

App mínima de **Streamlit** para estimar la elasticidad precio de la demanda con una regresión **OLS log-log**.

## Alcance

1. Cargar un archivo de datos históricos `.csv` o `.xlsx` (primera hoja, máximo 10 MB).
2. Elegir columna de **precio** y columna de **volumen**.
3. Pulsar **Calcular elasticidad**.
4. Obtener exclusivamente el coeficiente estimado de elasticidad.

No genera optimizaciones, gráficos, recomendaciones de precio ni proyecciones de profit.

## Modelo

`ln(volumen) = β₀ + β₁ × ln(precio) + error`

**Elasticidad precio = β₁.** Por ejemplo, β₁ = -1.5 significa que un incremento de 1% en precio se asocia aproximadamente con una reducción del 1.5% de volumen, bajo los supuestos del modelo.

> OLS simple identifica una relación histórica, no necesariamente un efecto causal del precio. Promociones, estacionalidad y tendencias pueden sesgar la estimación si afectan precio y volumen.

## Requisitos de datos

- Mínimo **8 observaciones**.
- Precio y volumen estrictamente **mayores que 0** en todas las filas.
- Columnas numéricas, sin valores vacíos ni símbolos monetarios.
- El precio debe variar; se rechazan datos inválidos en vez de excluir filas silenciosamente.
- Cada fila debe representar observaciones comparables para un mismo producto/mercado y periodo homogéneo.

Archivo de ejemplo: [`data/example.csv`](data/example.csv). Es **sintético**, no representa ventas reales.

## Ejecutar en Windows (PowerShell)

Ubicado en la carpeta de este módulo:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

Abrir la dirección local que indique Streamlit (normalmente `http://localhost:8501`).

## Pruebas

```powershell
python -m pip install pytest
python -m pytest -q
```

## Archivos

- `app.py`: interfaz Streamlit.
- `elasticity.py`: validación de entradas y estimación OLS log-log.
- `tests/test_elasticity.py`: pruebas del estimador.
- `data/example.csv`: datos de prueba sintéticos.

## Roadmap (fuera de esta fase)

Este módulo será parte de OPERATION KETER. Las fases posteriores podrán incorporar diagnósticos econométricos, control de variables, pricing y optimización; **no forman parte de la Fase 1**.
