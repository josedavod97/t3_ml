# CasaValor: predicción de precios de vivienda

API y aplicación web educativa que estima precios de vivienda en pesos colombianos mediante regresión lineal. La interfaz permite escribir o deslizar el área y actualiza la estimación y la gráfica.

> El modelo usa nueve datos de ejemplo y solo considera el área. No es una tasación ni representa los precios actuales del mercado.

## Ejecutar localmente en Windows

Desde la carpeta raíz del proyecto:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r ml_models\linear_regression\backend\requirements.txt -r ml_models\linear_regression\frontend\requirements.txt
```

Inicia cada servicio en una terminal independiente:

```powershell
# Backend
$env:FRONTEND_URL = "http://127.0.0.1:5000"
python -m uvicorn ml_models.linear_regression.backend.main:app --host 127.0.0.1 --port 8000
```

```powershell
# Frontend
$env:BACKEND_URL = "http://127.0.0.1:8000"
python -m flask --app ml_models.linear_regression.frontend.main run --host 127.0.0.1 --port 5000
```

Direcciones locales:

- Frontend: <http://127.0.0.1:5000>
- API: <http://127.0.0.1:8000>
- Swagger: <http://127.0.0.1:8000/docs>

## API

### `GET /`

Health check:

```json
{
  "status": "ok",
  "message": "API de predicción activa"
}
```

### `POST /predict`

Envía el área en metros cuadrados:

```json
{
  "area_m2": 100
}
```

Respuesta:

```json
{
  "area_m2": 100.0,
  "estimated_price_cop": 1376333333,
  "currency": "COP"
}
```

El área debe ser un número mayor que cero. Una solicitud no válida devuelve `422`.

## Ejecutar las pruebas

```powershell
python -m unittest discover -s tests -v
```

### `GET /chart-data`

Devuelve los datos de entrenamiento, la pendiente y el intercepto que utiliza el frontend para dibujar la gráfica.

## Entrenar el modelo

```powershell
python ml_models\linear_regression\backend\train.py
```

El script entrena el modelo, lo guarda en `ml_models\linear_regression\backend\model\linear_model.joblib` y abre la gráfica de dispersión. También guarda la gráfica como `price_prediction_plot.png` dentro de `backend`.

La API entrena el modelo automáticamente si todavía no existe el archivo guardado.

## Módulo experimental Random Forest

Se agregó en `ml_models\random_forest` una demostración independiente de clasificación de enfermedades. Usa un dataset sintético y no forma parte de CasaValor ni de sus servicios Railway; no debe usarse para diagnóstico o decisiones médicas.

```powershell
python -m pip install -r ml_models\random_forest\requirements.txt
python ml_models\random_forest\2.Entrenar_modelo.py
python -m streamlit run ml_models\random_forest\3.Predecir_enfermedad.py
```

El dataset incluido está en `ml_models\random_forest\data`. Para regenerarlo, ejecuta `python ml_models\random_forest\1.Crear_dataset.py`. El modelo entrenado se guarda en `ml_models\random_forest\models` y está excluido de Git.

## Desplegar en Railway

El proyecto usa dos servicios independientes dentro del mismo proyecto de Railway:

```powershell
# Backend: Dockerfile propio, API con Uvicorn.
railway up .\ml_models\linear_regression\backend --path-as-root --service casa-valor

# Frontend: Dockerfile propio, web con Gunicorn.
railway add --service casa-valor-frontend
railway up .\ml_models\linear_regression\frontend --path-as-root --service casa-valor-frontend
```

Genera un dominio para cada servicio con `railway domain --service casa-valor` y `railway domain --service casa-valor-frontend`. Configura `BACKEND_URL` en el frontend con el dominio del backend y `FRONTEND_URL` en el backend con el dominio del frontend. La web se sirve con Gunicorn; la API, con Uvicorn. Ambos servicios escuchan en el puerto `$PORT` asignado por Railway.

Railway detecta el `Dockerfile` de cada carpeta y construye ambos servicios con Docker. Para construir las imágenes localmente desde la raíz:

```powershell
docker build -t casa-valor-backend .\ml_models\linear_regression\backend
docker build -t casa-valor-frontend .\ml_models\linear_regression\frontend
```

## Estructura

```text
t3_ml\
├── main.py
├── requirements.txt
├── README.md
└── ml_models\
    ├── linear_regression\
    │   ├── backend\
    │   │   ├── .dockerignore
    │   │   ├── Dockerfile
    │   │   ├── main.py
    │   │   ├── requirements.txt
    │   │   ├── train.py
    │   │   └── model\
    │   │       └── linear_model.joblib  (generado al entrenar)
    │   └── frontend\
    │       ├── .dockerignore
    │       ├── Dockerfile
    │       ├── main.py
    │       ├── requirements.txt
    │       ├── app.js
    │       ├── index.html
    │       └── style.css
    └── random_forest\
        ├── 1.Crear_dataset.py
        ├── 2.Entrenar_modelo.py
        ├── 3.Predecir_enfermedad.py
        ├── README.md
        ├── requirements.txt
        ├── data\
        │   └── dataset_medico_ampliado.csv
        └── models\
            └── modelo_random_forest_ampliado.pkl  (generado al entrenar)
```
