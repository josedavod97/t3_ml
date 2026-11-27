import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import uvicorn

if __package__:
    from .train import X, load_model, y
else:
    from train import X, load_model, y


app = FastAPI(
    title="Predicción de precios de vivienda",
    description="Estima el precio de una vivienda en Colombia según su área.",
    version="1.0.0",
)
model = load_model()

frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[frontend_url.rstrip("/")],
        allow_methods=["GET", "POST"],
        allow_headers=["Content-Type"],
    )


class PredictionRequest(BaseModel):
    area_m2: float = Field(gt=0, allow_inf_nan=False, description="Área de la vivienda en metros cuadrados")


class PredictionResponse(BaseModel):
    area_m2: float
    estimated_price_cop: int
    currency: str = "COP"


class TrainingPoint(BaseModel):
    area_m2: float
    price_cop: int


class ChartDataResponse(BaseModel):
    points: list[TrainingPoint]
    slope_cop_per_m2: float
    intercept_cop: float


@app.get("/", summary="Health Check")
def health_check() -> dict[str, str]:
    return {"status": "ok", "message": "API de predicción activa"}


@app.get("/chart-data", response_model=ChartDataResponse)
def read_chart_data() -> ChartDataResponse:
    points = [
        TrainingPoint(area_m2=float(area), price_cop=int(price))
        for area, price in zip(X.ravel(), y)
    ]
    return ChartDataResponse(
        points=points,
        slope_cop_per_m2=float(model.coef_[0]),
        intercept_cop=float(model.intercept_),
    )


@app.post("/predict", response_model=PredictionResponse)
def predict_price(request: PredictionRequest) -> PredictionResponse:
    prediction = float(model.predict([[request.area_m2]])[0])
    return PredictionResponse(
        area_m2=request.area_m2,
        estimated_price_cop=round(prediction),
    )


if __name__ == "__main__":
    uvicorn.run(
        "ml_models.linear_regression.backend.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
