import streamlit as st
import pandas as pd

# 1. Configuración básica
st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi - COMPRAS")

# 2. Tu ID de Google Sheet (extraído de tu enlace)
SHEET_ID = "1Cy4K3ddIM7Z4hproTb9b-tFW39gSYjKA2XmSb-_65YA"
# Tu GID de la pestaña COMPRAS
GID = "578329158"

# URL de exportación ultra-directa
url = f"https://docs.google.com{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data(ttl=60) # Cache de 1 minuto para no saturar
def cargar_datos():
    try:
        # Cargamos los datos sin florituras para evitar el Errno -2
        return pd.read_csv(url)
    except Exception as e:
        return f"Error: {e}"

# 3. Lógica de visualización
datos = cargar_datos()

if isinstance(datos, pd.DataFrame):
    st.success("✅ ¡Conectado!")
    
    # Buscador para que sea útil
    busqueda = st.text_input("🔍 Buscar en COMPRAS:")
    if busqueda:
        mask = datos.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)
        st.dataframe(datos[mask], use_container_width=True)
    else:
        st.dataframe(datos, use_container_width=True)
else:
    st.error("⚠️ No se puede conectar ahora mismo.")
    st.info("Esto es un fallo de red de Streamlit. Pulsa el botón de abajo para forzar la conexión.")
    if st.button("🔄 Reintentar Conexión"):
        st.cache_data.clear()
        st.rerun()
