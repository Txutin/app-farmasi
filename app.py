import streamlit as st
import pandas as pd

st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi - COMPRAS")

# Intentamos con la URL de "publicación web" que es más ligera para los servidores
# He extraído el ID de tu hoja directamente
SHEET_ID = "1Cy4K3ddIM7Z4hproTb9b-tFW39gSYjKA2XmSb-_65YA"
GID = "578329158"

# Esta estructura de URL suele saltarse los errores de "Name or service not known"
url = f"https://docs.google.com{SHEET_ID}/pub?gid={GID}&output=csv"

@st.cache_data(ttl=10)
def cargar_datos_emergencia():
    try:
        # Forzamos la lectura con un motor diferente (python) para mayor compatibilidad
        df = pd.read_csv(url, engine='python', on_bad_lines='skip')
        return df
    except Exception as e:
        return str(e)

data = cargar_datos_emergencia()

if isinstance(data, pd.DataFrame):
    st.success("✅ ¡Conexión recuperada con éxito!")
    
    busqueda = st.text_input("🔍 Buscar registro:")
    if busqueda:
        mask = data.astype(str).apply(lambda x: x.str.contains(busqueda, case=False, na=False)).any(axis=1)
        st.dataframe(data[mask], use_container_width=True)
    else:
        st.dataframe(data, use_container_width=True)
else:
    st.error("⚠️ El servidor de Streamlit sigue sin ver a Google.")
    st.code(data)
    st.info("Paso final: Ve a tu Excel -> Archivo -> Compartir -> Publicar en la web -> Pulsa el botón 'Publicar'.")

if st.button("♻️ Forzar Reintento"):
    st.cache_data.clear()
    st.rerun()
