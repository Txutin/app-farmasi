import streamlit as st
import pandas as pd

# 1. Configuración de la página para que parezca app móvil
st.set_page_config(page_title="Farmasi App", layout="centered")

st.title("💄 Gestión Farmasi")

# 2. Conexión con Google Sheets (enlace en formato export csv)
sheet_id = "TU_ID_DE_HOJA_AQUÍ"
url = f"https://docs.google.com{sheet_id}/export?format=csv"

@st.cache_data
def load_data():
    return pd.read_csv(url)

df = load_data()

# 3. Interfaz de la App
st.write("### Inventario Actual")
st.dataframe(df) # Aquí vería sus productos

# Buscador rápido
busqueda = st.text_input("Buscar producto:")
if busqueda:
    resultado = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]
    st.write(resultado)
