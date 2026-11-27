# 🏠 t3_ml

<p align="center">
  <strong>Proyectos de aprendizaje automático hechos para practicar.</strong><br>
  CasaValor estima precios de vivienda y Random Forest muestra una clasificación experimental.
</p>

<p align="center">
  <a href="https://github.com/josedavod97/t3_ml"><img src="https://img.shields.io/badge/GitHub-t3__ml-181717?logo=github" alt="Repositorio GitHub"></a>
  <img src="https://img.shields.io/badge/Python-3-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Despliegue-Railway-8B5CF6" alt="Railway">
  <img src="https://img.shields.io/badge/Demo-Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
</p>

> **Aviso:** son proyectos educativos. CasaValor usa pocos datos de ejemplo y Random Forest utiliza datos médicos sintéticos; ninguno debe usarse para tomar decisiones reales.

## Enlaces del proyecto

| Proyecto | Enlace |
|---|---|
| CasaValor — aplicación web | [Abrir aplicación](https://casa-valor-frontend-production.up.railway.app/) |
| CasaValor — API | [Abrir API](https://casa-valor-production.up.railway.app/) |
| Documentación de la API | [Abrir Swagger](https://casa-valor-production.up.railway.app/docs) |
| Demostración Random Forest | [Abrir en Streamlit](https://josedavod.streamlit.app/) |
| Código fuente | [Ver repositorio en GitHub](https://github.com/josedavod97/t3_ml) |

## Índice

- [Proyectos](#proyectos)
- [CasaValor en local](#casavalor-en-local)
- [API](#api)
- [Pruebas](#pruebas)
- [Demostración Random Forest](#demostración-random-forest)
- [Despliegue en Railway](#despliegue-en-railway)
- [Estructura](#estructura)

## Proyectos

| Proyecto | ¿Qué hace? | Tecnologías |
|---|---|---|
| **CasaValor** | Estima el precio de una vivienda a partir de su área. | FastAPI, Flask, scikit-learn, Docker |
| **Random Forest** | Clasifica datos médicos sintéticos en una interfaz interactiva. | Streamlit, scikit-learn, Plotly |

## CasaValor en local

Los siguientes pasos son para Windows y PowerShell. Desde la carpeta raíz, crea el entorno e instala las dependencias:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r ml_models\linear_regression\backend\requirements.txt -r ml_models\linear_regression\frontend\requirements.txt
```

Inicia el backend en una terminal:

```powershell
$env:FRONTEND_URL = "http://127.0.0.1:5000"
python -m uvicorn ml_models.linear_regression.backend.main:app --host 127.0.0.1 --port 8000
```

Inicia el frontend en otra terminal:

```powershell
$env:BACKEND_URL = "http://127.0.0.1:8000"
python -m flask --app ml_models.linear_regression.frontend.main run --host 127.0.0.1 --port 5000
```

| Servicio local | Dirección |
|---|---|
| Aplicación web | <http://127.0.0.1:5000> |
| API | <http://127.0.0.1:8000> |
| Swagger | <http://127.0.0.1:8000/docs> |

## API

| Método y ruta | Descripción |
|---|---|
| `GET /` | Confirma que la API está activa. |
| `GET /chart-data` | Devuelve los datos y valores que usa la gráfica. |
| `POST /predict` | Estima el precio para un área en metros cuadrados. |

Ejemplo de solicitud a `POST /predict`:

```json
{
  "area_m2": 100
}
```

Respuesta de ejemplo:

```json
{
  "area_m2": 100.0,
  "estimated_price_cop": 1376333333,
  "currency": "COP"
}
```

El área debe ser mayor que cero. Si el dato no es válido, la API responde con `422`.

## Pruebas

Desde la raíz del proyecto, ejecuta:

```powershell
python -m unittest discover -s tests -v
```

## Demostración Random Forest

Esta demo es independiente de CasaValor. Trabaja con un conjunto de datos sintéticos y **no es una herramienta de diagnóstico médico**.

Instala sus dependencias y ejecuta Streamlit:

```powershell
python -m pip install -r ml_models\random_forest\requirements.txt
python -m streamlit run ml_models\random_forest\3.Predecir_enfermedad.py
```

Si el modelo no existe al iniciar, la aplicación lo entrena con el dataset incluido. Para ver las métricas de entrenamiento manualmente:

```powershell
python ml_models\random_forest\2.Entrenar_modelo.py
```

El dataset está en `ml_models\random_forest\data`. Puedes generarlo de nuevo con:

```powershell
python ml_models\random_forest\1.Crear_dataset.py
```

Los modelos generados se guardan en `ml_models\random_forest\models` y no se suben a Git.

## Despliegue en Railway

CasaValor usa dos servicios separados, cada uno con su propio Dockerfile:

| Servicio | Tecnología | URL |
|---|---|---|
| Frontend | Flask y Gunicorn | [casa-valor-frontend-production](https://casa-valor-frontend-production.up.railway.app/) |
| Backend | FastAPI y Uvicorn | [casa-valor-production](https://casa-valor-production.up.railway.app/) |

Con Railway CLI, desde la raíz del repositorio:

```powershell
# Backend
railway up .\ml_models\linear_regression\backend --path-as-root --service casa-valor

# Frontend
railway add --service casa-valor-frontend
railway up .\ml_models\linear_regression\frontend --path-as-root --service casa-valor-frontend
```

Cada servicio necesita un dominio de Railway. Configura `BACKEND_URL` en el frontend con el dominio de la API y `FRONTEND_URL` en el backend con el dominio del frontend. Railway asigna el puerto mediante la variable `$PORT`.

Para construir las imágenes con Docker desde la raíz:

```powershell
docker build -t casa-valor-backend .\ml_models\linear_regression\backend
docker build -t casa-valor-frontend .\ml_models\linear_regression\frontend
```

## Estructura

```text
t3_ml/
├── main.py
├── README.md
├── requirements.txt
├── ml_models/
│   ├── linear_regression/
│   │   ├── backend/
│   │   │   ├── Dockerfile
│   │   │   ├── main.py
│   │   │   ├── requirements.txt
│   │   │   └── train.py
│   │   └── frontend/
│   │       ├── Dockerfile
│   │       ├── app.js
│   │       ├── index.html
│   │       ├── main.py
│   │       ├── requirements.txt
│   │       └── style.css
│   └── random_forest/
│       ├── 1.Crear_dataset.py
│       ├── 2.Entrenar_modelo.py
│       ├── 3.Predecir_enfermedad.py
│       ├── model_utils.py
│       ├── requirements.txt
│       └── data/
└── tests/
    ├── test_api.py
    ├── test_frontend.py
    └── test_random_forest_model.py
```
