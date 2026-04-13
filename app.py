import streamlit as st
import requests

# URL de tu Apps Script
API_URL = "https://script.google.com/macros/s/AKfycbxo5qRFWUyS2Q3K_OZfDcuxZ0r6Q9V1RvrrMarV6xJ5nNbCkw2t2sSW0ysLMNE02fK7/exec"

st.set_page_config(page_title="Registro QR", layout="centered")

st.title("📦 Registro por QR")

st.write("Escanea el QR, introduce cantidad y OT")

# --- QR por input automático ---
qr_data = st.text_input(
    "📷 Código QR",
    placeholder="Escanea el QR con la cámara del móvil",
)

st.info(
    "📱 Consejo: toca este campo y escanea el QR con la cámara del móvil."
)

# --- FORMULARIO ---
with st.form("registro"):
    cantidad = st.number_input("Cantidad", min_value=1, step=1)
    ot = st.text_input("OT")
    enviar = st.form_submit_button("💾 Guardar")

# --- ENVÍO ---
if enviar:
    if not qr_data:
        st.error("El código QR es obligatorio")
    elif not ot:
        st.error("La OT es obligatoria")
    else:
        payload = {
            "qr": qr_data,
            "cantidad": cantidad,
            "ot": ot
        }

        r = requests.post(API_URL, json=payload)

        if r.status_code == 200:
            st.success("✅ Registro guardado correctamente")
        else:
            st.error("❌ Error al guardar")

        if response.status_code == 200:
            st.success("✅ Registro guardado correctamente")
        else:
            st.error("❌ Error al guardar el registro")
