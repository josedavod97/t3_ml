# Demostración Random Forest

Este módulo aislado clasifica enfermedades con datos sintéticos. Es una demostración educativa, no una herramienta de diagnóstico ni de toma de decisiones médicas.

Si el archivo del modelo no existe, la aplicación lo entrena automáticamente con el dataset incluido al iniciar. El modelo generado se guarda localmente y no hace falta subirlo a GitHub.

Desde la raíz del proyecto, en PowerShell:

```powershell
python -m pip install -r ml_models\random_forest\requirements.txt
# Opcional: entrena el modelo y muestra métricas
python ml_models\random_forest\2.Entrenar_modelo.py
python -m streamlit run ml_models\random_forest\3.Predecir_enfermedad.py
```

El dataset inicial está en `data\dataset_medico_ampliado.csv`. Para regenerarlo, ejecuta:

```powershell
python ml_models\random_forest\1.Crear_dataset.py
```

El modelo entrenado se crea en `models\modelo_random_forest_ampliado.pkl`.
