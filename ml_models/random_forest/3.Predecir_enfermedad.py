from pathlib import Path

import joblib
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

CARPETA = Path(__file__).resolve().parent
RUTA_MODELO = CARPETA / "models" / "modelo_random_forest_ampliado.pkl"

st.set_page_config(page_title="Demostración Random Forest", page_icon="🩺", layout="wide")

st.markdown("""
<style>
.diagnostico-card { padding:1.5rem; border-radius:1rem; margin:1rem 0; text-align:center; box-shadow:0 4px 6px rgba(0,0,0,0.1); }
.metric-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding:1rem; border-radius:0.5rem; color:white; text-align:center; }
.stButton>button { width:100%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; font-weight:bold; }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    if not RUTA_MODELO.is_file():
        raise FileNotFoundError(
            f"No se encontró el modelo en {RUTA_MODELO}. "
            "Ejecuta primero 2.Entrenar_modelo.py."
        )
    return joblib.load(RUTA_MODELO)

model = load_model()
features = model.feature_names_in_

st.title("🩺 Demostración educativa de clasificación de enfermedades")
st.markdown("### Clasificación experimental con 34 variables clínicas simuladas")
st.warning(
    "Demostración educativa entrenada con datos sintéticos. No sirve para diagnosticar "
    "ni para tomar decisiones médicas. Ante síntomas preocupantes, consulta a un profesional "
    "o a los servicios de emergencia."
)

with st.expander("📚 **Tabla de ayuda: Síntomas típicos por enfermedad**"):
    st.markdown("""
    Selecciona los siguientes síntomas para simular cada condición:

    | Enfermedad | Síntomas / Hallazgos clave |
    |------------|----------------------------|
    | 💔 **Infarto** | Edad >45, hipertensión, diabetes, colesterol alto, fumador. Dolor torácico **opresivo** con irradiación a brazo/mandíbula, **sudoración fría**, palpitaciones, disnea. FC >100, SatO₂ <95%. |
    | 🫁 **Neumonía** | Fiebre >38°C, **escalofríos**, **tos productiva** (posible esputo hemoptoico), disnea, dolor torácico pleurítico. SatO₂ <94%. |
    | 🤧 **Gripe** | Fiebre, escalofríos, tos seca, fatiga, mareos, náuseas. Ausencia de disnea severa o dolor opresivo. |
    | 🧠 **Ansiedad** | Palpitaciones, sudoración fría, disnea (sin hipoxia), mareos, **ansiedad subjetiva** (moderada/severa), ataques de pánico, insomnio. Sin fiebre ni tos. |
    | 🤢 **Gastroenteritis** | Náuseas, vómitos, diarrea, dolor abdominal, fiebre posible (baja), fatiga. Sin síntomas respiratorios ni cardíacos. |
    """)
    st.caption("💡 Usa esta guía para probar el modelo. Los valores numéricos (edad, constantes) también influyen.")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Signos Vitales", "❤️ Factores Riesgo", "🫀 Síntomas Cardiorrespiratorios", "🧠 Otros Síntomas"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        edad = st.number_input("Edad (años)", 0, 120, 45)
        sexo = st.radio("Sexo", ["Mujer", "Hombre"], horizontal=True)
        frecuencia_cardiaca = st.number_input("Frecuencia cardíaca (lpm)", 30, 200, 75)
        presion_sistolica = st.number_input("Presión sistólica (mmHg)", 70, 250, 120)
    with c2:
        presion_diastolica = st.number_input("Presión diastólica (mmHg)", 40, 150, 80)
        saturacion_oxigeno = st.number_input("SatO₂ (%)", 70, 100, 98)
        temperatura = st.number_input("Temperatura (°C)", 35.0, 42.0, 36.5, step=0.1)

with tab2:
    c1, c2, c3 = st.columns(3)
    with c1:
        hipertension = st.selectbox("Hipertensión", ["No", "Sí"])
        diabetes = st.selectbox("Diabetes", ["No", "Sí"])
    with c2:
        colesterol_alto = st.selectbox("Colesterol alto", ["No", "Sí"])
        fumador = st.selectbox("Fumador activo", ["No", "Sí"])
    with c3:
        obesidad = st.selectbox("Obesidad (IMC>30)", ["No", "Sí"])
        antecedente_cardiaco = st.selectbox("Antecedente cardíaco familiar", ["No", "Sí"])

with tab3:
    c1, c2 = st.columns(2)
    with c1:
        dolor_pecho = st.selectbox("Dolor torácico", ["No", "Sí"])
        if dolor_pecho == "Sí":
            dolor_opresivo = st.selectbox("Dolor opresivo", ["No", "Sí"])
            dolor_irradiado = st.selectbox("Irradiación a brazo/mandíbula", ["No", "Sí"])
        else:
            dolor_opresivo = "No"
            dolor_irradiado = "No"
        palpitaciones = st.selectbox("Palpitaciones", ["No", "Sí"])
    with c2:
        disnea = st.selectbox("Disnea (dificultad respirar)", ["No", "Sí"])
        sudoracion_fria = st.selectbox("Sudoración fría", ["No", "Sí"])
        tos = st.selectbox("Tos", ["No", "Sí"])
        if tos == "Sí":
            tos_productiva = st.selectbox("Tos productiva", ["No", "Sí"])
            if tos_productiva == "Sí":
                esputo_hemoptoico = st.selectbox("Esputo con sangre", ["No", "Sí"])
            else:
                esputo_hemoptoico = "No"
        else:
            tos_productiva = "No"
            esputo_hemoptoico = "No"

with tab4:
    c1, c2 = st.columns(2)
    with c1:
        fiebre = st.selectbox("Fiebre (>38°C)", ["No", "Sí"])
        escalofrios = st.selectbox("Escalofríos", ["No", "Sí"])
        mareos = st.selectbox("Mareos", ["No", "Sí"])
        ansiedad = st.selectbox("Ansiedad subjetiva", ["No", "Leve", "Moderada", "Severa"])
        ataques_panico = st.selectbox("Ataques de pánico", ["No", "Sí"])
        insomnio = st.selectbox("Insomnio reciente", ["No", "Sí"])
    with c2:
        nauseas = st.selectbox("Náuseas", ["No", "Sí"])
        vomitos = st.selectbox("Vómitos", ["No", "Sí"])
        diarrea = st.selectbox("Diarrea", ["No", "Sí"])
        dolor_abdominal = st.selectbox("Dolor abdominal", ["No", "Sí"])
        fatiga = st.selectbox("Fatiga general", ["No", "Sí"])
        perdida_apetito = st.selectbox("Pérdida de apetito", ["No", "Sí"])

# ================= CONVERTIR A VALORES NUMÉRICOS =================
def s2b(x): return 1 if x == "Sí" else 0
def ans2int(x):
    return {"No":0, "Leve":1, "Moderada":1, "Severa":2}.get(x, 0)

input_dict = {
    "edad": edad,
    "sexo": 1 if sexo == "Hombre" else 0,
    "frecuencia_cardiaca": frecuencia_cardiaca,
    "presion_sistolica": presion_sistolica,
    "presion_diastolica": presion_diastolica,
    "saturacion_oxigeno": saturacion_oxigeno,
    "temperatura": temperatura,
    "hipertension": s2b(hipertension),
    "diabetes": s2b(diabetes),
    "colesterol_alto": s2b(colesterol_alto),
    "fumador": s2b(fumador),
    "obesidad": s2b(obesidad),
    "antecedente_cardiaco": s2b(antecedente_cardiaco),
    "dolor_pecho": s2b(dolor_pecho),
    "dolor_opresivo": s2b(dolor_opresivo),
    "dolor_irradiado": s2b(dolor_irradiado),
    "palpitaciones": s2b(palpitaciones),
    "disnea": s2b(disnea),
    "sudoracion_fria": s2b(sudoracion_fria),
    "tos": s2b(tos),
    "tos_productiva": s2b(tos_productiva),
    "esputo_hemoptoico": s2b(esputo_hemoptoico),
    "fiebre": s2b(fiebre),
    "escalofrios": s2b(escalofrios),
    "mareos": s2b(mareos),
    "ansiedad": ans2int(ansiedad),
    "ataques_panico": s2b(ataques_panico),
    "insomnio": s2b(insomnio),
    "nauseas": s2b(nauseas),
    "vomitos": s2b(vomitos),
    "diarrea": s2b(diarrea),
    "dolor_abdominal": s2b(dolor_abdominal),
    "fatiga": s2b(fatiga),
    "perdida_apetito": s2b(perdida_apetito),
}

# Reordenar según el orden original de features (importante)
input_df = pd.DataFrame([{col: input_dict[col] for col in features}])

# ================= PREDICCIÓN =================
if st.button("🔍 Ver clasificación experimental", use_container_width=True):
    pred = model.predict(input_df)[0]
    probas = model.predict_proba(input_df)[0]
    resultados = pd.DataFrame({
        "Enfermedad": model.classes_,
        "Probabilidad": (probas * 100).round(2)
    }).sort_values("Probabilidad", ascending=False)

    info_map = {
        "infarto": ("Infarto", "#ef4444", "💔"),
        "neumonia": ("Neumonía", "#f59e0b", "🫁"),
        "gripe": ("Gripe", "#10b981", "🤧"),
        "ansiedad": ("Ansiedad", "#8b5cf6", "🧠"),
        "gastroenteritis": ("Gastroenteritis", "#f97316", "🤢")
    }
    nombre, color, icono = info_map.get(pred, (pred.upper(), "#6366f1", "🩺"))

    st.markdown("---")
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown(f"""
        <div class='diagnostico-card' style='background:{color}20; border:2px solid {color};'>
            <h1 style='font-size:3rem'>{icono}</h1>
            <h2 style='color:{color}'>{nombre}</h2>
            <p>Categoría: {pred.upper()}</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        prob_main = resultados.loc[resultados["Enfermedad"]==pred, "Probabilidad"].values[0]
        st.markdown(f"<div class='metric-card'><p>PUNTAJE DEL MODELO</p><h3>{prob_main:.1f}%</h3></div>", unsafe_allow_html=True)

    colors_plot = [info_map.get(e, (None,"#94a3b8"))[1] for e in resultados["Enfermedad"]]
    fig = go.Figure(go.Bar(
        x=resultados["Probabilidad"], y=resultados["Enfermedad"], orientation="h",
        marker=dict(color=colors_plot, line=dict(color="white", width=1.5)),
        text=resultados["Probabilidad"].apply(lambda x: f"{x:.1f}%"),
        textposition="outside",
    ))
    fig.update_layout(height=400, xaxis_title="Probabilidad (%)", xaxis_range=[0, 105])
    st.plotly_chart(fig, width="stretch")

    st.info(
        "Esta clasificación y sus probabilidades no son una evaluación médica. "
        "No las uses para decidir tratamientos ni para retrasar atención profesional."
    )