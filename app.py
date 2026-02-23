import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="Gestión Farmasi 3.0", layout="wide")
st.title("💄 Gestión Farmasi 3.0")

# 2. Conexión directa a la pestaña "IMPORT_AI"
# Usamos el parámetro 'sheet_name' para asegurar que lea la pestaña correcta
url = "https://docs.google.com"

@st.cache_data(ttl=60)
def cargar_datos():
    # Cargamos los datos de la pestaña IMPORT_AI
    return pd.read_csv(url)

# 3. Mostrar los datos
try:
    df = cargar_datos()
    st.success(f"✨ ¡Conexión exitosa con la pestaña IMPORT_AI!")
    
    # Buscador amigable
    busqueda = st.text_input("🔍 Buscar por Orden, Producto o Cliente:", placeholder="Escribe aquí...")
    
    if busqueda:
        # Filtro que busca en todas las columnas (incluyendo ORDEN_NO)
        resultado = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]
        st.dataframe(resultado, use_container_width=True)
    else:
        st.write("### 📦 Registros actuales")
        st.dataframe(df, use_container_width=True)

except Exception as e:
    st.error("⚠️ Error de lectura: No se encuentran datos en 'IMPORT_AI'.")
    st.info("Verifica que la pestaña 'IMPORT_AI' no esté vacía en tu Google Sheets.")
    if st.button("🔄 Reintentar conexión"):
        st.cache_data.clear()
        st.rerun()
