import streamlit as st
import streamlit.components.v1 as components
import requests

API_URL = "https://script.google.com/macros/s/AKfycbxo5qRFWUyS2Q3K_OZfDcuxZ0r6Q9V1RvrrMarV6xJ5nNbCkw2t2sSW0ysLMNE02fK7/exec"

st.set_page_config(page_title="Registro QR", layout="centered")
st.title("📦 Registro por QR")

st.write("1️⃣ Escanea el QR con la cámara")
st.write("2️⃣ Introduce cantidad y OT")
st.write("3️⃣ Guarda el registro")

# --- LECTOR QR CON CAMARA ---
qr_code = components.html(
    """
    <div id="reader" style="width:100%"></div>

    <script src="https://unpkg.com/html5-qrcode"></script>
    <script>
        const qr = new Html5Qrcode("reader");
        qr.start(
            { facingMode: "environment" },
            { fps: 10, qrbox: 250 },
            qrCodeMessage => {
                window.parent.postMessage(
                    { type: "qr", value: qrCodeMessage },
                    "*"
                );
                qr.stop();
            }
        );
    </script>
    """,
    height=320,
)

# --- RECIBIR QR DESDE JS ---
if "qr_value" not in st.session_state:
    st.session_state.qr_value = ""

st.markdown("""
<script>
window.addEventListener("message", (event) => {
  if (event.data.type === "qr") {
    const input = window.parent.document.querySelector('input[data-testid="stTextInput"]');
    if (input) {
      input.value = event.data.value;
      input.dispatchEvent(new Event('input', { bubbles: true }));
    }
  }
});
</script>
""", unsafe_allow_html=True)

qr_value = st.text_input("📷 Código QR")

# --- FORMULARIO ---
with st.form("registro_form"):
    cantidad = st.number_input("Cantidad", min_value=1, step=1)
    ot = st.text_input("OT")
    guardar = st.form_submit_button("💾 Guardar")

# --- ENVÍO A GOOGLE SHEETS ---
if guardar:
    if not qr_value:
        st.error("Escanea un QR primero")
    elif not ot:
        st.error("La OT es obligatoria")
    else:
        payload = {
            "qr": qr_value,
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
