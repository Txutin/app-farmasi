import streamlit as st
import pandas as pd

# 1. Configuración visual
st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi 3.0")

# 2. Conexión limpia a la pestaña IMPORT_AI
url = "https://docs.google.com"

@st.cache_data(ttl=60)
def cargar_datos():
    # Leemos todo como texto (dtype=str) para evitar errores de formato
    # y limitamos a las primeras 20 columnas para que no se pierda en el infinito
    return pd.read_csv(url, dtype=str, on_bad_lines='skip', usecols=range(0, 15))

# 3. Mostrar los datos
try:
    df = cargar_datos()
    
    # Eliminamos filas que estén totalmente vacías
    df = df.dropna(how='all')
    
    st.success("✨ ¡Inventario cargado! (Filas procesadas correctamente)")
    
    # Buscador amigable
    busqueda = st.text_input("🔍 Buscar producto o cliente:", placeholder="Escribe aquí...")
    
    if busqueda:
        mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        st.write("### 📦 Vista de tus datos")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Error al organizar los datos: {e}")
    st.info("Esto sucede si la hoja tiene celdas combinadas o formatos muy complejos.")
    if st.button("🔄 Limpiar Memoria y Reintentar"):
        st.cache_data.clear()
        st.rerun()
