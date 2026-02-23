import streamlit as st
import pandas as pd

# 1. Configuración visual
st.set_page_config(page_title="App Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi 3.0")

# 2. LA NUEVA URL (Copia y pega esto tal cual)
url = "https://docs.google.com"

@st.cache_data(ttl=60)
def cargar_datos():
    # Esta función lee los datos de tu pestaña específica
    return pd.read_csv(url)

# 3. Lógica para mostrar los datos
try:
    df = cargar_datos()
    st.success("✨ ¡Conexión con el inventario de Farmasi exitosa!")
    
    busqueda = st.text_input("🔍 Buscar producto:")
    
    if busqueda:
        resultado = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]
        st.dataframe(resultado, use_container_width=True)
    else:
        st.write("### 📦 Lista de productos")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("⚠️ Error: No se detectan datos en la pestaña indicada.")
    st.info("Asegúrate de que la pestaña de tu Google Sheets tenga títulos en la primera fila.")
