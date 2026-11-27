from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression


# Superficie en metros cuadrados y precio en pesos colombianos.
X = np.array([[70], [80], [90], [100], [110], [120], [130], [140], [150]])
y = np.array(
    [
        420_000_000,
        600_000_000,
        900_000_000,
        1_500_000_000,
        1_800_000_000,
        2_100_000_000,
        2_400_000_000,
        2_700_000_000,
        3_000_000_000,
    ]
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "linear_model.joblib"
PLOT_PATH = BASE_DIR / "price_prediction_plot.png"


def train_model() -> LinearRegression:
    model = LinearRegression()
    model.fit(X, y)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    print(f"Modelo entrenado y guardado en: {MODEL_PATH}")
    return model


def load_model() -> LinearRegression:
    if not MODEL_PATH.is_file():
        return train_model()

    model = joblib.load(MODEL_PATH)
    if not isinstance(model, LinearRegression):
        raise TypeError(f"El archivo del modelo no contiene una regresión lineal: {MODEL_PATH}")
    return model


def plot_training_data(model: LinearRegression, show: bool = True) -> None:
    areas = X.ravel()
    plt.scatter(areas, y, color="crimson", label="Precios reales")
    plt.plot(areas, model.predict(X), color="navy", label="Regresión lineal")
    plt.title("Precio de vivienda según su área")
    plt.xlabel("Área (m²)")
    plt.ylabel("Precio (COP)")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(PLOT_PATH)
    print(f"Gráfica guardada en: {PLOT_PATH}")
    if show:
        plt.show()
    else:
        plt.close()


if __name__ == "__main__":
    trained_model = train_model()
    plot_training_data(trained_model)
