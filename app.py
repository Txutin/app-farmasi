import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi - COMPRAS")

# URL construida pieza a pieza para evitar errores de caracteres
SHEET_ID = "1Cy4K3ddIM7Z4hproTb9b-tFW39gSYjKA2XmSb-_65YA"
GID = "578329158"
url = f"https://docs.google.com{SHEET_ID}/export?format=csv&gid={GID}"

try:
    # Intentamos la carga sin caché para diagnosticar
    df = pd.read_csv(url, on_bad_lines='skip')
    
    st.success("✨ Conexión recuperada")
    
    # Buscador
    busqueda = st.text_input("🔍 Buscar en registros:", placeholder="Escribe para filtrar...")
    
    if busqueda:
        mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False, na=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("❌ Error de red o URL")
    st.warning("El servidor no encuentra la dirección de Google Sheets.")
    st.code(str(e))
    
    # Botón de auxilio
    if st.button("🔌 Reintentar Conexión"):
        st.rerun()
