import streamlit as st
import pandas as pd
import requests
import io

st.set_page_config(page_title="Gestión Farmasi 4.0", layout="wide")
st.title("💄 Gestión Farmasi 4.0 - COMPRAS")

# --- URL CORREGIDA MANUALMENTE (SIN VARIABLES PARA EVITAR EL ERROR DE PEGADO) ---
# He usado el ID que salía en tu error: 1sVaeJDe_feAMiuL9ct7rGUS18Vy9vEipPXqHlw0MnPU
url_final = "https://docs.google.com"

def cargar_datos():
    try:
        # Petición directa con cabecera de navegador
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url_final, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Leemos el CSV forzando todo a texto para no perder ceros
            return pd.read_csv(io.StringIO(response.text), dtype=str)
        else:
            return f"Error Google: {response.status_code}. Revisa si la pestaña se llama COMPRAS."
    except Exception as e:
        return f"Fallo de red: {str(e)}"

# Ejecución
df = cargar_datos()

if isinstance(df, pd.DataFrame):
    st.success("✨ ¡CONEXIÓN ESTABLECIDA! Farmasi 4.0 está en línea.")
    
    # Buscador funcional
    busqueda = st.text_input("🔍 Buscar en COMPRAS (Factura, Producto, Código...):")
    if busqueda:
        mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False, na=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)
else:
    st.error("🚨 Sigue habiendo un problema de conexión")
    st.info("La URL que está intentando usar el servidor es:")
    st.code(url_final)
    st.warning(df)

if st.button("🔄 Forzar Actualización"):
    st.rerun()
