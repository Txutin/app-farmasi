import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi - COMPRAS")

# Conexión oficial que usa Service Account
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Usamos solo el ID de tu hoja para evitar errores de URL
    SHEET_ID = "1Cy4K3ddIM7Z4hproTb9b-tFW39gSYjKA2XmSb-_65YA"
    
    df = conn.read(
        spreadsheet=f"https://docs.google.com{SHEET_ID}/edit",
        worksheet="COMPRAS",
        ttl="1m"
    )
    
    st.success("✨ ¡Conexión privada establecida!")
    st.dataframe(df, use_container_width=True)
    
except Exception as e:
    st.error(f"⚠️ Error de acceso: {e}")
    st.info("Necesitas configurar el archivo 'secrets' en Streamlit Cloud.")
