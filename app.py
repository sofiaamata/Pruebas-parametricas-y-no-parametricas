import streamlit as st
import requests
import json

# -------------------------------------------------------------------
# DATA_URL = https://raw.githubusercontent.com/sofiaMata/quizADA/main/items.json
# -------------------------------------------------------------------

st.set_page_config(page_title="Quiz Estadística ADA", layout="centered")

st.title("📊 Quiz interactivo — Selección de Pruebas Estadísticas")
st.write("Responde cada pregunta y avanza una por una. ¡Buena suerte!")

# -------------------------------------------------------------------
# CARGAR ÍTEMS DESDE GITHUB RAW
# -------------------------------------------------------------------
# 👇 Cambia esta URL por la tuya (formato RAW)
URL = "https://raw.githubusercontent.com/TU_USUARIO/TU_REPO/main/items.json"

try:
    response = requests.get(URL)
    items = response.json()
except:
    st.error("⚠️ No se pudo cargar el archivo items.json desde GitHub. Revisa el link RAW.")
    st.stop()

# -------------------------------------------------------------------
# INICIALIZAR ESTADOS
# -------------------------------------------------------------------

if "index" not in st.session_state:
    st.session_state.index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "finished" not in st.session_state:
    st.session_state.finished = False

# -------------------------------------------------------------------
# MOSTRAR RESULTADOS FINALES
# -------------------------------------------------------------------

if st.session_state.finished:
    st.header("🎉 Resultados finales")
    st.subheader(f"Puntaje obtenido: **{st.session_state.score} / {len(items)}**")

    if st.session_state.score == len(items):
        st.success("¡Perfecto! Dominas todas las pruebas estadísticas 👏")
    elif st.session_state.score >= len(items) * 0.7:
        st.info("Muy buen trabajo, solo faltaron unos detalles 😊")
    else:
        st.warning("Puedes intentarlo de nuevo para mejorar 💪")

    if st.button("🔄 Reiniciar Quiz"):
        st.session_state.index = 0
        st.session_state.score = 0
        st.session_state.finished = False
        st.experimental_rerun()

    st.stop()

# -------------------------------------------------------------------
# MOSTRAR PREGUNTA ACTUAL
# -------------------------------------------------------------------

item = items[st.session_state.index]

st.subheader(f"Pregunta {st.session_state.index + 1} de {len(items)}")
st.write(item["pregunta"])

opcion = st.radio("Selecciona tu respuesta:", item["opciones"])

# -------------------------------------------------------------------
# BOTÓN PARA RESPONDER
# -------------------------------------------------------------------

if st.button("Responder"):
    correcta = item["correcta"]
    index_seleccionado = item["opciones"].index(opcion)

    # Evaluar respuesta
    if index_seleccionado == correcta:
        st.success("✔️ ¡Correcto!")
        st.session_state.score += 1
    else:
        st.error("❌ Incorrecto")

    # Mostrar explicación
    st.info(f"📘 Explicación: {item['explicacion']}")

    # Botón para avanzar
    if st.session_state.index + 1 < len(items):
        if st.button("➡️ Siguiente pregunta"):
            st.session_state.index += 1
            st.experimental_rerun()
    else:
        if st.button("🎯 Ver resultados finales"):
            st.session_state.finished = True
            st.experimental_rerun()
