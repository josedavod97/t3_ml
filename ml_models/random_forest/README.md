# Demostración Random Forest

Este módulo aislado clasifica enfermedades con datos sintéticos. Es una demostración educativa, no una herramienta de diagnóstico ni de toma de decisiones médicas.

Desde la raíz del proyecto, en PowerShell:

```powershell
python -m pip install -r ml_models\random_forest\requirements.txt
python ml_models\random_forest\2.Entrenar_modelo.py
python -m streamlit run ml_models\random_forest\3.Predecir_enfermedad.py
```

El dataset inicial está en `data\dataset_medico_ampliado.csv`. Para regenerarlo, ejecuta:

```powershell
python ml_models\random_forest\1.Crear_dataset.py
```

El modelo entrenado se crea en `models\modelo_random_forest_ampliado.pkl`.
