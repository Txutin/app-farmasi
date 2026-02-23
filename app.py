import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="App Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi 3.0")

# 2. Tu llave de conexión (La URL que creamos arriba)
url = "https://docs.google.com"

@st.cache_data(ttl=60)
def cargar_datos():
    # Cargamos el CSV directamente desde Google
    return pd.read_csv(url)

# 3. Lógica de la aplicación
try:
    df = cargar_datos()
    st.success("✨ ¡Conexión con el inventario exitosa!")
    
    # Buscador por descripción o código
    busqueda = st.text_input("🔍 Buscar producto (nombre o código):")
    
    if busqueda:
        # Filtramos en todas las columnas
        resultado = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]
        st.write(f"Resultados para: **{busqueda}**")
        st.dataframe(resultado, use_container_width=True)
    else:
        st.write("### 📦 Lista completa de productos")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("⚠️ No se pudo conectar con la hoja de cálculo.")
    st.info("Revisa que el archivo de Google Sheets tenga datos y columnas con nombre.")
