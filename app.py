import streamlit as st
import pdfplumber
import pandas as pd
import io

st.set_page_config(page_title="Farmasi 4.0 - SCAN", layout="centered")

st.title("🚀 Escáner de Facturas Farmasi")

archivo_pdf = st.file_uploader("📥 Sube tu Factura PDF", type=["pdf"])

if archivo_pdf is not None:
    with st.spinner("🤖 Analizando estructura completa..."):
        try:
            with pdfplumber.open(io.BytesIO(archivo_pdf.read())) as pdf:
                # 1. Extraer el TEXTO de todas las páginas
                texto_total = ""
                for pagina in pdf.pages:
                    texto_total += pagina.extract_text() or ""
                
                # 2. Extraer las TABLAS (donde suelen estar los productos y precios)
                tablas_detectadas = []
                for pagina in pdf.pages:
                    tabla = pagina.extract_table()
                    if tabla:
                        tablas_detectadas.append(pd.DataFrame(tabla))

            # --- PANEL DE RESULTADOS ---
            st.success("✅ Análisis finalizado")

            # Mostramos las tablas encontradas (aquí verás si ha leído bien los productos)
            if tablas_detectadas:
                st.subheader("📦 Productos detectados en la tabla:")
                for i, df_tabla in enumerate(tablas_detectadas):
                    st.dataframe(df_tabla, use_container_width=True)
            
            # Mostramos todo el texto capturado para que verifiques si falta algo
            with st.expander("🔍 Ver TODO el texto extraído (Sin filtros)"):
                st.text_area("Contenido completo del PDF:", value=texto_total, height=300)
                # Botón de ayuda para que me pases el texto si falla algo
                st.info("Si falta algún dato importante, copia el texto de arriba y dímelo.")

        except Exception as e:
            st.error(f"Error técnico al abrir el PDF: {e}")

st.divider()
st.caption("Farmasi 4.0 - Modo Diagnóstico Activo")
