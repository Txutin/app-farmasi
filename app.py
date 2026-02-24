import streamlit as st
import pdfplumber
import io

# 1. Configuración Limpia (Look de App Móvil)
st.set_page_config(page_title="Farmasi 4.0 - Lector", layout="centered")

# Estilo para que el botón se vea más grande en el dedo
st.markdown("""
    <style>
    .stFileUploader { scale: 1.1; }
    .stMarkdown h1 { font-size: 1.5rem !important; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("📄 Lector de Facturas Farmasi")

# --- EL ÚNICO BOTÓN QUE NECESITAS ---
# Al pulsarlo en Android, abrirá automáticamente tu carpeta de descargas
archivo_pdf = st.file_uploader("Pulsa aquí para subir tu factura PDF", type=["pdf"])

# 2. Qué pasa cuando eliges el archivo
if archivo_pdf is not None:
    with st.spinner("Procesando factura..."):
        try:
            # Leemos el PDF en memoria
            with pdfplumber.open(io.BytesIO(archivo_pdf.read())) as pdf:
                texto = ""
                for pagina in pdf.pages:
                    texto += pagina.extract_text() + "\n"
            
            # --- RESULTADO INMEDIATO ---
            st.success("✅ Factura leída correctamente")
            
            # Mostramos el contenido para que yo pueda ayudarte a extraer los datos
            st.subheader("Contenido de la Factura:")
            st.code(texto)
            
            st.info("💡 Copia el texto de arriba y pégamelo aquí para que enseñe a la App a reconocer tu Orden, Fecha y Total automáticamente.")

        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

# 3. Limpieza de interfaz
st.divider()
st.caption("Farmasi 4.0 - Gestión de Compras")
