import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi - COMPRAS")

# 1. Variables limpias (Sin errores de pegado)
SHEET_ID = "1Cy4K3ddIM7Z4hproTb9b-tFW39gSYjKA2XmSb-_65YA"
GID = "578329158"

# 2. Construcción manual de la URL para evitar que se junten (Ojo a la '/' extra)
url_limpia = "https://docs.google.com" + SHEET_ID + "/export?format=csv&gid=" + GID

def cargar_datos_seguros():
    try:
        # Petición directa con timeout para no dejar colgada la web
        response = requests.get(url_limpia, timeout=10)
        # Si la respuesta es exitosa (200), leemos el contenido
        if response.status_code == 200:
            return pd.read_csv(io.StringIO(response.text))
        else:
            return f"Error de Google: {response.status_code}. Revisa si la hoja es pública."
    except Exception as e:
        return f"Error de conexión: {str(e)}"

# 3. Mostrar datos
df = cargar_datos_seguros()

if isinstance(df, pd.DataFrame):
    st.success("✅ ¡CONECTADO POR FIN!")
    
    # Buscador rápido
    busqueda = st.text_input("🔍 Buscar registro:")
    if busqueda:
        mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False, na=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)
else:
    st.error("🚨 Sigue habiendo un problema con la URL")
    st.code(url_limpia) # Esto nos permite ver si la URL es correcta en pantalla
    st.warning(df)

if st.button("🔄 Forzar Recarga"):
    st.rerun()
