import streamlit as st
import pandas as pd

# 1. Configuración visual
st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi 3.0")

# 2. URL de exportación directa (esta no falla si la hoja es pública)
# He limpiado la URL para que sea la versión más compatible
url = "https://docs.google.com"

@st.cache_data(ttl=60)
def cargar_datos():
    # Intentamos leer la hoja directamente
    return pd.read_csv(url)

# 3. Lógica para mostrar los datos
try:
    df = cargar_datos()
    st.success("✨ ¡Conexión establecida con éxito!")
    
    # Buscador
    busqueda = st.text_input("🔍 Buscar producto o registro:", placeholder="Escribe aquí...")
    
    if busqueda:
        # Filtro en todas las columnas
        resultado = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]
        st.dataframe(resultado, use_container_width=True)
    else:
        st.write("### 📦 Datos actuales en la hoja")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Error de lectura: {e}")
    st.info("Asegúrate de que la primera fila de tu Excel tenga los títulos (ej: ORDEN_NO).")
    if st.button("🔄 Reintentar"):
        st.cache_data.clear()
        st.rerun()
