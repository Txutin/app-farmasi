import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi - Compras")

# 2. URL de conexión directa a la pestaña "COMPRAS"
# Nota: He usado el GID que suele corresponder a las pestañas adicionales
url = "https://docs.google.com"

@st.cache_data(ttl=60)
def cargar_datos():
    # Leemos la pestaña COMPRAS ignorando errores de formato
    return pd.read_csv(url, on_bad_lines='skip', low_memory=False)

# 3. Mostrar los datos
try:
    df = cargar_datos()
    st.success("✨ ¡Conexión establecida con la pestaña COMPRAS!")
    
    # Buscador potente
    busqueda = st.text_input("🔍 Buscar en Compras (Producto, ID, Fecha...):")
    
    if busqueda:
        mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        st.write("### 📦 Historial de Compras")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ No se pudo cargar la pestaña 'COMPRAS'")
    st.info("Verifica que el nombre de la pestaña en tu Excel sea exactamente COMPRAS (en mayúsculas).")
    if st.button("🔄 Reintentar"):
        st.cache_data.clear()
        st.rerun()
