import streamlit as st
import pandas as pd

# 1. Configuración de la interfaz (Siempre lo primero)
st.set_page_config(page_title="Gestión Farmasi 4.0", layout="wide")
st.title("💄 Gestión Farmasi 4.0 - PANEL DE CONTROL")

# --- TU ENLACE DE PUBLICACIÓN CSV (EL QUE ME ACABAS DE DAR) ---
URL_PUB = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSlBHB_vd1Dz_X1Ngor981-ySiL-Gwp__QxTxxHrNEL78aOEHbcIRPdAZriu5UKMedN9zcTyplwqYnd/pub?gid=0&single=true&output=csv"

@st.cache_data(ttl=10) # Refresco automático cada 10 segundos
def cargar_datos_publicos():
    try:
        # Cargamos los datos forzando todo a texto para no perder los ceros de los códigos
        df = pd.read_csv(URL_PUB, dtype=str, on_bad_lines='skip', engine='python')
        # Limpiamos posibles filas o columnas vacías que añade Google al publicar
        df = df.dropna(how='all', axis=0).dropna(how='all', axis=1)
        return df
    except Exception as e:
        return f"Error al leer el CSV: {e}"

# 2. Ejecución de la carga
df = cargar_datos_publicos()

if isinstance(df, pd.DataFrame):
    st.success(f"🚀 ¡CONECTADO! Se han detectado {len(df)} registros en Farmasi 4.0")
    
    # Buscador Inteligente
    busqueda = st.text_input("🔍 Buscar por FACTURA, PRODUCTO o CÓDIGO:", placeholder="Escribe algo para filtrar...")
    
    if busqueda:
        # Filtro global en todas las columnas
        mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False, na=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        # Vista de la tabla completa si no hay búsqueda
        st.dataframe(df, use_container_width=True)
    
    # Si la tabla está vacía, damos instrucciones
    if df.empty:
        st.info("La tabla está conectada pero no tiene datos. Escribe tus encabezados en el Google Sheet.")
        st.write("Headers esperados:", ["ORDEN_NO", "FACTURA_NO", "FECHA_FACTURA", "DESCRIPCION", "TOTAL..."])

else:
    st.error("🚨 Error crítico de conexión")
    st.warning(df)

# Botón manual de refresco
if st.button("🔄 Forzar Sincronización"):
    st.cache_data.clear()
    st.rerun()
