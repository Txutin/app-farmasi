import streamlit as st
import pandas as pd

# 1. Configuración de la página (DEBE IR PRIMERO PARA QUE NO FALLE)
st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.sidebar.title("🛠️ Opciones de Farmasi")

# 2. URL de conexión a la pestaña COMPRAS
# Nota: Usamos el parámetro 'sheet' para que Google busque por el nombre que pusiste
url = "https://docs.google.com"

@st.cache_data(ttl=30) # Se refresca cada 30 segundos por si los scripts actualizan algo
def cargar_datos_seguros():
    try:
        # Forzamos la lectura como texto para que los scripts no den errores de formato
        return pd.read_csv(url, dtype=str, on_bad_lines='skip', low_memory=False)
    except Exception:
        return None

# 3. Lógica de la Interfaz
st.title("💄 Gestión Farmasi - COMPRAS")

# Intentamos cargar los datos
df = cargar_datos_seguros()

if df is not None:
    st.sidebar.success("✅ Conexión con Google Sheets activa")
    
    # Buscador amigable
    busqueda = st.text_input("🔍 ¿Qué registro buscas en COMPRAS?", placeholder="Ej: Labial, ID de pedido...")
    
    if busqueda:
        # Filtro inteligente que ignora errores de los scripts
        mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        st.write("### 📦 Historial de Compras Actualizado")
        st.dataframe(df, use_container_width=True)
else:
    st.error("⚠️ Los scripts de Google están bloqueando la conexión temporalmente.")
    st.info("Asegúrate de que la pestaña se llama exactamente COMPRAS (en mayúsculas) y no tiene celdas combinadas en la primera fila.")
    if st.button("🔄 Forzar Recarga de Datos"):
        st.cache_data.clear()
        st.rerun()
