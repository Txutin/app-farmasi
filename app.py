import streamlit as st
import pandas as pd

# Configuración visual
st.set_page_config(page_title="Farmasi App", layout="centered")
st.title("💄 Gestión Farmasi")

# URL Directa de descarga (Formato CSV)
# Hemos unido el ID y el GID en un solo enlace limpio
url = "https://docs.google.com"

@st.cache_data(ttl=60) # Se refresca cada minuto
def load_data():
    return pd.read_csv(url)

try:
    df = load_data()
    st.success("✨ ¡Conexión establecida con Farmasi!")
    
    # Buscador amigable
    busqueda = st.text_input("🔍 ¿Qué producto buscas?", placeholder="Ej: Labial, Crema...")
    
    if busqueda:
        # Filtro inteligente
        mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)
        resultado = df[mask]
        st.dataframe(resultado, use_container_width=True)
    else:
        st.write("### 📦 Inventario Actual")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("⚠️ Error de conexión temporal")
    st.info("Pulsa la tecla 'R' para reintentar la conexión con Google Sheets.")
    # Botón de reintento manual
    if st.button("🔄 Reintentar ahora"):
        st.cache_data.clear()
        st.rerun()
