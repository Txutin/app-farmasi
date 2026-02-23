import streamlit as st
import pandas as pd

# Configuración para que parezca una App móvil
st.set_page_config(page_title="Farmasi App", layout="centered")

st.title("💄 Gestión Farmasi")

# Tu ID real de Google Sheets
sheet_id = "1Cy4K3ddIM7Z4hproTb9b-tFW39gSYjKA2XmSb-_65YA"
# Usamos el GID 453328905 que es el de tu pestaña específica
url = f"https://docs.google.com{sheet_id}/export?format=csv&gid=453328905"

@st.cache_data(ttl=600) # Se actualiza cada 10 minutos
def load_data():
    return pd.read_csv(url)

try:
    df = load_data()
    st.success("¡Conectado con éxito!")
    
    # Buscador para tu mujer
    busqueda = st.text_input("🔍 Buscar producto por nombre:")
    
    if busqueda:
        # Filtramos en todas las columnas
        resultado = df[df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]
        st.write(resultado)
    else:
        st.write("### Inventario completo:")
        st.dataframe(df)

except Exception as e:
    st.error(f"Error al conectar: {e}")
    st.info("Asegúrate de que la hoja de Google esté en 'Cualquier persona con el enlace puede leer'.")
