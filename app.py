import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Configuración de la página
st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi 3.0")

# Enlace directo a tu hoja (el normal de edición)
url = "https://docs.google.com"

# Creamos la conexión oficial de Streamlit para Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Leemos la pestaña "IMPORT_AI" directamente
    df = conn.read(spreadsheet=url, worksheet="IMPORT_AI", ttl="1m")
    
    st.success("✨ ¡Conexión establecida con IMPORT_AI!")
    
    # Buscador interactivo
    busqueda = st.text_input("🔍 Buscar producto o cliente:")
    if busqueda:
        resultado = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]
        st.dataframe(resultado, use_container_width=True)
    else:
        st.write("### 📦 Registros actuales")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error(f"⚠️ Error de conexión: {e}")
    st.info("Si el error persiste, intenta pulsar el botón de 'Reboot' en el panel de Streamlit.")
