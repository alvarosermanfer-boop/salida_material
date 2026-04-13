import streamlit as st
import streamlit.components.v1 as components
import requests

API_URL = "https://script.google.com/macros/s/AKfycbxo5qRFWUyS2Q3K_OZfDcuxZ0r6Q9V1RvrrMarV6xJ5nNbCkw2t2sSW0ysLMNE02fK7/exec"

st.set_page_config(page_title="Registro QR", layout="centered")
st.title("📦 Registro por QR")

st.write("Escanea el QR con la cámara")

# --- LECTOR QR ---
qr_value = components.html(
    """
    <html>
      <head>
        <script src="https://unpkg.com/html5-qrcode"></script>
      </head>
      <body>
        <div id="reader" style="width:100%"></div>

        <script>
          const qrCodeSuccessCallback = (decodedText, decodedResult) => {
            window.parent.postMessage(
              { type: "qr", value: decodedText },
              "*"
            );
            html5QrcodeScanner.clear();
          };

          const html5QrcodeScanner = new Html5Qrcode("reader");
          html5QrcodeScanner.start(
            { facingMode: "environment" },
            { fps: 10, qrbox: 250 },
            qrCodeSuccessCallback
          );
        </script>
      </body>
    </html>
    """,
    height=320,
)


# --- RECIBIR QR ---
if "qr_result" not in st.session_state:
    st.session_state.qr_result = ""

components.html(
    """
    <script>
      window.addEventListener("message", (event) => {
        window.parent.postMessage(
          { streamlitQr: event.data },
          "*"
        );
      });
    </script>
    """,
    height=0,
)

# Campo visible (solo lectura)
qr_text = st.text_input(
    "📷 Código QR",
    value=st.session_state.qr_result,
    disabled=True
)

# --- FORMULARIO ---
with st.form("registro"):
    cantidad = st.number_input("Cantidad", min_value=1, step=1)
    ot = st.text_input("OT")
    guardar = st.form_submit_button("💾 Guardar")

# --- GUARDADO ---
if guardar:
    if not qr_text:
        st.error("Escanea un QR primero")
    elif not ot:
        st.error("La OT es obligatoria")
    else:
        payload = {
            "qr": qr_text,
            "cantidad": cantidad,
            "ot": ot
        }

        r = requests.post(API_URL, json=payload)

        if r.status_code == 200:
            st.success("✅ Registro guardado")
            st.session_state.qr_result = ""
        else:
            st.error("❌ Error al guardar")


        if response.status_code == 200:
            st.success("✅ Registro guardado correctamente")
        else:
            st.error("❌ Error al guardar el registro")
