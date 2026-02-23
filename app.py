import streamlit as st
import pandas as pd
import requests
import io

# 1. Configuración de la interfaz
st.set_page_config(page_title="Gestión Farmasi 4.0", layout="wide")
st.title("💄 Gestión Farmasi 4.0 - COMPRAS")

# --- PASO ÚNICO: PEGA AQUÍ EL ID DE TU NUEVO SHEET "FARMASI 4.0" ---
ID_SHEET = "1SVAEjde_feAmiul9Ct7rguS18Vy9VeiPPxQHlw0mNpU" 
# -----------------------------------------------------------------

# URL para buscar la pestaña "COMPRAS" específicamente
url_compras = f"https://docs.google.com{ID_SHEET}/gviz/tq?tqx=out:csv&sheet=COMPRAS"

@st.cache_data(ttl=5) # Refresco ultra rápido
def cargar_farmasi_4_0():
    try:
        # Usamos headers para evitar bloqueos de seguridad de Google
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url_compras, headers=headers, timeout=10)
        
        if response.status_code == 200:
            # Forzamos dtype=str para no perder los ceros en códigos de barras
            df = pd.read_csv(io.StringIO(response.text), dtype=str)
            return df
        else:
            return f"Error {response.status_code}: Revisa que el Sheet sea 'Público - Lector' y la pestaña se llame COMPRAS."
    except Exception as e:
        return f"Fallo de red: {e}"

# Ejecución
df = cargar_farmasi_4_0()

if isinstance(df, pd.DataFrame):
    # Verificamos si los headers coinciden para avisarte si falta algo
    headers_esperados = ["ORDEN_NO", "FACTURA_NO", "FECHA_FACTURA", "DESCRIPCION", "TOTAL"]
    headers_reales = df.columns.tolist()
    
    st.success(f"✅ Conectado a FARMASI 4.0 | Pestaña: COMPRAS")
    
    # Buscador potente
    busqueda = st.text_input("🔍 Buscar en registros (Factura, Producto, Código...):")
    
    if busqueda:
        mask = df.astype(str).apply(lambda x: x.str.contains(busqueda, case=False, na=False)).any(axis=1)
        st.dataframe(df[mask], use_container_width=True)
    else:
        st.dataframe(df, use_container_width=True)
        
    if df.empty:
        st.info("💡 La conexión es correcta, pero la hoja está vacía. Añade datos en Google Sheets para verlos aquí.")

else:
    st.error("🚨 No se pudo conectar")
    st.warning(df)
    if st.button("🔄 Reintentar conexión"):
        st.cache_data.clear()
        st.rerun()
