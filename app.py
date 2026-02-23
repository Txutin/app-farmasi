import streamlit as st
import pandas as pd

# 1. Configuración visual
st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi 3.0")

# 2. URL de conexión (Pestaña IMPORT_AI)
url = "https://docs.google.com"

@st.cache_data(ttl=60)
def cargar_datos():
    # Usamos on_bad_lines='skip' para que no explote si hay filas raras
    # Y low_memory=False para manejar hojas grandes de Farmasi
    return pd.read_csv(url, on_bad_lines='skip', low_memory=False)

# 3. Lógica para mostrar los datos
try:
    df = cargar_datos()
    
    # Limpiamos columnas totalmente vacías que suelen causar el error
    df = df.dropna(axis=1, how='all')
    
    st.success("✨ ¡Inventario de Farmasi cargado con éxito!")
    
    # Buscador potente
    busqueda = st.text_input("🔍 ¿Qué estás buscando?", placeholder="Escribe el nombre del producto, orden o cliente...")
    
    if busqueda:
        # Filtro que busca en todo el documento
        mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        st.write("### 📦 Vista general de la hoja")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Error al procesar los datos: {e}")
    st.info("Prueba a pulsar el botón de abajo para refrescar la memoria de la app.")
    if st.button("🔄 Forzar Recarga de Datos"):
        st.cache_data.clear()
        st.rerun()
