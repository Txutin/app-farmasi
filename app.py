import streamlit as st
import pandas as pd

# 1. Configuración inmediata
st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")

st.title("💄 Gestión Farmasi - COMPRAS")

# 2. URL simplificada al máximo (formato pubvis)
SHEET_ID = "1Cy4K3ddIM7Z4hproTb9b-tFW39gSYjKA2XmSb-_65YA"
GID = "578329158"
url = f"https://docs.google.com{SHEET_ID}/export?format=csv&gid={GID}"

# 3. Carga directa sin decoradores que bloqueen
try:
    # Quitamos el @st.cache_data para que no se quede colgado en el bucle
    df = pd.read_csv(url)
    
    st.success("✅ ¡Cargado con éxito!")
    
    # Buscador simple para verificar que responde
    busqueda = st.text_input("🔍 Filtrar compras:")
    if busqueda:
        df = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]
    
    st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("🔌 Error de conexión rápida")
    st.info("Copia este error para decirme qué pasa:")
    st.code(str(e))

if st.button("🔄 Forzar actualización"):
    st.rerun()
