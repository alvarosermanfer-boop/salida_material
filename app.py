import streamlit as st
import streamlit.components.v1 as components
import requests

API_URL = "https://script.google.com/macros/s/AKfycbxo5qRFWUyS2Q3K_OZfDcuxZ0r6Q9V1RvrrMarV6xJ5nNbCkw2t2sSW0ysLMNE02fK7/exec"

st.set_page_config(page_title="Registro por QR", layout="centered")
st.title("📦 Registro por QR")

st.write("Escanea el QR con la cámara o escríbelo manualmente")

# Estado para guardar el QR
if "qr_value" not in st.session_state:
    st.session_state.qr_value = ""

# --- HTML + JS LECTOR QR ---
components.html(
    """
    <html>
      <head>
        <script src="https://unpkg.com/html5-qrcode"></script>
      </head>
      <body>
        <div id="reader" style="width:100%; height:300px;"></div>

        <script>
          function onScanSuccess(decodedText, decodedResult) {
              window.parent.postMessage(
                { type: "qr", value: decodedText },
                "*"
              );
              html5QrcodeScanner.clear();
          }

          var html5QrcodeScanner = new Html5QrcodeScanner(
            "reader",
            {
              fps: 10,
              rememberLastUsedCamera: true,
              supportedScanTypes: [Html5QrcodeScanType.SCAN_TYPE_CAMERA]
            },
            false
          );
          html5QrcodeScanner.render(onScanSuccess);
        </script>
      </body>
    </html>
    """,
    height=350,
)

# --- CAPTURA DEL MENSAJE DESDE JS ---
components.html(
    """
    <script>
      window.addEventListener("message", (event) => {
        if (event.data.type === "qr") {
          fetch("/_stcore/update_session_state", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              key: "qr_value",
              value: event.data.value
            })
          });
        }
      });
    </script>
    """,
    height=0,
)

# --- CAMPO EDITABLE (MANUAL O AUTO) ---
qr_text = st.text_input(
    "📷 Código QR",
    value=st.session_state.qr_value,
    help="Puedes modificarlo manualmente si es necesario"
)

st.session_state.qr_value = qr_text

# --- FORMULARIO ---
with st.form("registro"):
    cantidad = st.number_input("Cantidad", min_value=1, step=1)
    ot = st.text_input("OT")
    guardar = st.form_submit_button("💾 Guardar")

# --- ENVÍO ---
if guardar:
    if not qr_text:
        st.error("El código QR es obligatorio")
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
            st.session_state.qr_value = ""
        else:
            st.error("❌ Error al guardar")

