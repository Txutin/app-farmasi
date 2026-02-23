import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi - COMPRAS")

# Conexión oficial de Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Esta función busca la pestaña "COMPRAS" de forma nativa
    df = conn.read(
        spreadsheet="https://docs.google.com",
        worksheet="COMPRAS",
        ttl="1m"
    )
    
    st.success("✨ ¡Conexión establecida con COMPRAS!")
    st.dataframe(df, use_container_width=True)
    
except Exception as e:
    st.error(f"⚠️ Error de lectura: {e}")
    st.info("Revisa que el nombre de la pestaña sea exactamente COMPRAS.")
