import streamlit as st
import requests
from pyzbar.pyzbar import decode
from PIL import Image

# 👉 PEGA AQUÍ TU URL DE APPS SCRIPT
API_URL = "https://script.google.com/macros/s/AKfycbxo5qRFWUyS2Q3K_OZfDcuxZ0r6Q9V1RvrrMarV6xJ5nNbCkw2t2sSW0ysLMNE02fK7/exec"

st.set_page_config(
    page_title="Registro QR",
    layout="centered"
)

st.title("📦 Registro por QR")

st.write("1️⃣ Escanea el QR")
st.write("2️⃣ Introduce cantidad y OT")
st.write("3️⃣ Guarda el registro")

# --- ESCANEO QR ---
qr_data = None
img = st.camera_input("📷 Escanear código QR")

if img:
    image = Image.open(img)
    decoded = decode(image)

    if decoded:
        qr_data = decoded[0].data.decode("utf-8")
        st.success(f"QR leído: {qr_data}")
    else:
        st.error("No se ha detectado ningún QR")

# --- FORMULARIO ---
with st.form("registro_form"):
    cantidad = st.number_input("Cantidad", min_value=1, step=1)
    ot = st.text_input("OT")
    enviar = st.form_submit_button("💾 Guardar")

# --- ENVÍO A GOOGLE SHEETS ---
if enviar:
    if not qr_data:
        st.error("Debes escanear un QR primero")
    elif not ot:
        st.error("La OT es obligatoria")
    else:
        payload = {
            "qr": qr_data,
            "cantidad": cantidad,
            "ot": ot
        }

        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            st.success("✅ Registro guardado correctamente")
        else:
            st.error("❌ Error al guardar el registro")
