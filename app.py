import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi - COMPRAS")

# URL TOTALMENTE ESTÁTICA (Sin sumas ni variables para evitar el error de pegado)
url_final = "https://docs.google.com"

def cargar_datos():
    try:
        # Usamos un timeout corto para que no se quede colgado
        response = requests.get(url_final, timeout=10)
        if response.status_code == 200:
            return pd.read_csv(io.StringIO(response.text))
        else:
            return f"Error de Google: {response.status_code}. Verifica que el Sheet sea Público."
    except Exception as e:
        return f"Error de red: {str(e)}"

# Intentar cargar
df = cargar_datos()

if isinstance(df, pd.DataFrame):
    st.success("✅ ¡CONECTADO POR FIN!")
    
    # Buscador rápido
    busqueda = st.text_input("🔍 Filtrar registros:", placeholder="Escribe para buscar...")
    if busqueda:
        mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False, na=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)
else:
    st.error("🚨 Problema con la conexión")
    st.info("La URL que estamos usando es:")
    st.code(url_final)
    st.warning(df)

if st.button("🔄 Refrescar"):
    st.rerun()
