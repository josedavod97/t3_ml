from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def crear_clasificador():
    return RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
    )


def cargar_o_entrenar_modelo(ruta_modelo: Path, ruta_dataset: Path):
    if ruta_modelo.is_file():
        return joblib.load(ruta_modelo)

    if not ruta_dataset.is_file():
        raise FileNotFoundError(
            f"No se encontró el dataset en {ruta_dataset}. "
            "Ejecuta primero 1.Crear_dataset.py."
        )

    datos = pd.read_csv(ruta_dataset)
    X = datos.drop(columns=["diagnostico"])
    y = datos["diagnostico"]

    modelo = crear_clasificador()
    modelo.fit(X, y)

    ruta_modelo.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(modelo, ruta_modelo)
    return modelo
