import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi 3.0")

# ID de tu documento de Google Sheets
SHEET_ID = "1Cy4K3ddIM7Z4hproTb9b-tFW39gSYjKA2XmSb-_65YA"

# 2. Selector de Pestañas Manual
# Aquí he puesto los códigos (GID) de tus pestañas. 
# El 453328905 es el que me dijiste de IMPORT_AI.
opciones = {
    "Pestaña Principal (Hoja 1)": "0",
    "IMPORT_AI (Gestión)": "453328905"
}

seleccion = st.sidebar.selectbox("📂 Elige qué pestaña quieres ver:", list(opciones.keys()))
gid = opciones[seleccion]

# 3. Función para cargar los datos de la pestaña elegida
@st.cache_data(ttl=60)
def cargar_datos(id_hoja, id_pestaña):
    url = f"https://docs.google.com{id_hoja}/export?format=csv&gid={id_pestaña}"
    # Leemos con cuidado para evitar el error de 'tokenizing'
    return pd.read_csv(url, on_bad_lines='skip', low_memory=False).dropna(how='all')

try:
    df = cargar_datos(SHEET_ID, gid)
    st.success(f"✨ Viendo ahora: {seleccion}")
    
    # Buscador
    busqueda = st.text_input("🔍 Buscar en esta tabla:", placeholder="Escribe producto, orden...")
    
    if busqueda:
        mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Error al conectar con {seleccion}")
    st.info("Prueba a cambiar de pestaña en el menú de la izquierda.")
