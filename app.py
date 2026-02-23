import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi - COMPRAS")

# Tu ID y GID exactos
SHEET_ID = "1Cy4K3ddIM7Z4hproTb9b-tFW39gSYjKA2XmSb-_65YA"
GID = "578329158"

# Intentamos la URL por defecto, pero con un mecanismo de reintento
url = f"https://docs.google.com{SHEET_ID}/export?format=csv&gid={GID}"

def cargar_datos_extremo():
    try:
        # Usamos un User-Agent para que Google no bloquee la petición del servidor
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return pd.read_csv(io.StringIO(response.text))
    except Exception as e:
        return f"Fallo de conexión: {str(e)}"

# Ejecución
df = cargar_datos_extremo()

if isinstance(df, pd.DataFrame):
    st.success("✅ ¡CONECTADO!")
    st.dataframe(df, use_container_width=True)
else:
    st.error("🚨 El servidor de Streamlit sigue bloqueado.")
    st.info("Para desbloquearlo SIN Google Cloud: Ve a la pestaña 'Settings' de tu app en Streamlit Cloud y pulsa 'Reboot App'. Eso fuerza al servidor a buscar una nueva ruta de red.")
    st.code(df)
