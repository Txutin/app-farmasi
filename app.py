import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Gestión Farmasi 3.0", page_icon="💄")
st.title("💄 Gestión Farmasi 3.0")

# URL de tu hoja de cálculo (LA ORIGINAL, SIN MODIFICAR)
sheet_url = "https://docs.google.com"

def load_data(url):
    # Este método es más resistente a errores de red
    csv_url = url.replace("/edit#gid=", "/export?format=csv&gid=")
    return pd.read_csv(csv_url)

try:
    df = load_data(sheet_url)
    st.success("✨ ¡Conexión establecida con la pestaña IMPORT_AI!")
    
    # Buscador
    busqueda = st.text_input("🔍 Buscar en el inventario:", placeholder="Ej: ORDEN_NO, Producto...")
    
    if busqueda:
        mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        st.write("### 📦 Datos en la hoja:")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("⚠️ Error de conexión crítica con Google.")
    st.info("Esto suele ser un problema temporal de los servidores de Streamlit.")
    if st.button("🔄 Forzar Reinicio del Sistema"):
        st.cache_data.clear()
        st.rerun()
