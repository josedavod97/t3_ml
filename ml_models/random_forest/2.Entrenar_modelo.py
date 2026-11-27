import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

from model_utils import crear_clasificador

CARPETA = Path(__file__).resolve().parent
RUTA_DATASET = CARPETA / "data" / "dataset_medico_ampliado.csv"
RUTA_MODELO = CARPETA / "models" / "modelo_random_forest_ampliado.pkl"

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def log(titulo):
    print("\n" + "=" * 70)
    print(titulo)
    print("=" * 70)


try:
    log("1. CARGA DEL DATASET")
    print(f"Ruta del dataset: {RUTA_DATASET}")
    datos = pd.read_csv(RUTA_DATASET)
    print(f"Dataset cargado: {datos.shape[0]} filas y {datos.shape[1]} columnas")

    log("2. PREPARACION DE LOS DATOS")
    X = datos.drop("diagnostico", axis=1)
    y = datos["diagnostico"]

    print(f"Variables utilizadas: {len(X.columns)}")
    for numero, columna in enumerate(X.columns, 1):
        print(f"{numero}. {columna}")
    print(f"Clases: {y.unique()}")

    X_entrenamiento, X_prueba, y_entrenamiento, y_prueba = train_test_split(
        X,
        y,
        test_size=0.3,
        random_state=42,
        stratify=y,
    )
    print(
        f"Datos para entrenar: {len(X_entrenamiento)} | "
        f"Datos para probar: {len(X_prueba)}"
    )

    log("3. ENTRENAMIENTO")
    modelo = crear_clasificador()
    modelo.fit(X_entrenamiento, y_entrenamiento)
    print("Modelo entrenado.")

    log("4. RESULTADOS")
    predicciones = modelo.predict(X_prueba)
    exactitud = modelo.score(X_prueba, y_prueba)
    print(f"Exactitud: {exactitud:.2%}")
    print(classification_report(y_prueba, predicciones))
    print("Matriz de confusion:")
    print(confusion_matrix(y_prueba, predicciones))

    log("5. VARIABLES IMPORTANTES")
    importancia = pd.DataFrame({
        "Variable": X.columns,
        "Importancia (%)": (modelo.feature_importances_ * 100).round(2),
    }).sort_values("Importancia (%)", ascending=False)
    print(importancia.head(15).to_string(index=False))

    log("6. GUARDAR MODELO")
    RUTA_MODELO.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, RUTA_MODELO)
    print(f"Modelo guardado en: {RUTA_MODELO}")
    print("El resultado es de practica porque el dataset usa datos sinteticos.")

except FileNotFoundError:
    log("ERROR")
    print(f"No se encontro el dataset: {RUTA_DATASET}")
    print("Ejecuta primero 1.Crear_dataset.py")
    raise SystemExit(1)
