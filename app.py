import streamlit as st
import pdfplumber
import pandas as pd
import re
import io

st.set_page_config(page_title="Farmasi 4.0 - SCAN", layout="centered")

# --- ESTILO APP ---
st.markdown("""
    <style>
    .stFileUploader { scale: 1.1; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #ff4b4b; color: white; }
    </style>
""", unsafe_allow_html=True)

st.title("🚀 Escáner de Facturas Farmasi")

# 1. El Botón de Carga (Único protagonista)
archivo_pdf = st.file_uploader("📥 Pulsa para subir Factura PDF", type=["pdf"])

if archivo_pdf is not None:
    with st.spinner("🤖 Extrayendo datos de Farmasi..."):
        try:
            with pdfplumber.open(io.BytesIO(archivo_pdf.read())) as pdf:
                texto = "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])
            
            # --- MOTOR DE EXTRACCIÓN AUTOMÁTICA ---
            # Buscamos los datos usando "Regular Expressions" (patrones)
            # Nota: Ajustaremos estos patrones según lo que me digas que sale
            orden = re.search(r"(?:Orden No|Pedido No):?\s*(\w+)", texto, re.I)
            factura = re.search(r"(?:Factura No|Factura):?\s*(\w+)", texto, re.I)
            total = re.search(r"(?:Total|Importe Total):?\s*([\d,.]+)", texto, re.I)
            fecha = re.search(r"(\d{2}/\d{2}/\d{4})", texto) # Busca fechas tipo 24/02/2026

            # --- VISTA PREVIA DE LOS DATOS ---
            st.success("✅ ¡Datos extraídos con éxito!")
            
            # Creamos una "Tarjeta de Confirmación"
            st.subheader("📋 Confirmar Datos")
            col1, col2 = st.columns(2)
            with col1:
                final_orden = st.text_input("ORDEN_NO", value=orden.group(1) if orden else "")
                final_factura = st.text_input("FACTURA_NO", value=factura.group(1) if factura else "")
            with col2:
                final_total = st.text_input("TOTAL (€)", value=total.group(1) if total else "0.00")
                final_fecha = st.text_input("FECHA_FACTURA", value=fecha.group(1) if fecha else "")

            # 2. EL BOTÓN MÁGICO
            if st.button("💾 GUARDAR EN GOOGLE SHEETS"):
                # Aquí es donde irá la conexión de escritura que activaremos a continuación
                st.balloons()
                st.info(f"Listo para guardar la orden {final_orden}. ¡Buen trabajo!")

        except Exception as e:
            st.error(f"Error al procesar: {e}")

# Mantenemos el visor de texto SOLO para depurar si algo falla
with st.expander("🛠️ Ver diagnóstico (Texto detectado)"):
    st.code(texto if 'texto' in locals() else "Sube un PDF para ver el texto")
