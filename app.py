import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.sidebar.title("🛠️ Opciones de Farmasi")

# 2. URL de conexión ajustada para exportar como CSV
# Usamos tu ID de hoja y el gid de la pestaña COMPRAS (578329158)
SHEET_ID = "1Cy4K3ddIM7Z4hproTb9b-tFW39gSYjKA2XmSb-_65YA"
GID = "578329158"
url = f"https://docs.google.com{SHEET_ID}/export?format=csv&gid={GID}"

@st.cache_data(ttl=30)
def cargar_datos_seguros():
    try:
        # Leemos directamente el CSV que genera Google
        return pd.read_csv(url, dtype=str)
    except Exception as e:
        st.error(f"Error técnico: {e}")
        return None

# 3. Lógica de la Interfaz
st.title("💄 Gestión Farmasi - COMPRAS")

df = cargar_datos_seguros()

if df is not None:
    st.sidebar.success("✅ Conexión con Google Sheets activa")
    
    busqueda = st.text_input("🔍 ¿Qué registro buscas en COMPRAS?", placeholder="Ej: Labial, ID de pedido...")
    
    if busqueda:
        mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False, na=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        st.write("### 📦 Historial de Compras Actualizado")
        st.dataframe(df, use_container_width=True)
else:
    st.error("⚠️ No se pudo leer la hoja.")
    st.info("Asegúrate de que en Google Sheets hayas dado a: Compartir -> Cualquier persona con el enlace.")
    if st.button("🔄 Forzar Recarga de Datos"):
        st.cache_data.clear()
        st.rerun()
