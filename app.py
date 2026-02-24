import streamlit as st

# --- NAVEGACIÓN TIPO APP ---
modo = st.sidebar.radio("Menú", ["📦 Ver Compras", "📄 Importar PDF"])

if modo == "📦 Ver Compras":
    # Aquí pegas el código que ya teníamos para ver la tabla
    st.title("Historial de Compras")
    # ... (tu código de ayer)
    
elif modo == "📄 Importar PDF":
    # Aquí pegas el código nuevo para subir el PDF
    st.title("Lector de Facturas")
    # ... (el código de pdfplumber)


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

import streamlit as st
import pandas as pd
import pdfplumber
import re

st.set_page_config(page_title="Farmasi 4.0 - Importador", layout="wide")

st.title("📄 Importador de Facturas Farmasi")
st.info("Sube el PDF descargado de la web para extraer los datos automáticamente.")

# --- ZONA DE CARGA (TIPO APP) ---
archivo_pdf = st.file_uploader("Arrastra aquí tu factura PDF", type=["pdf"])

if archivo_pdf is not None:
    with st.spinner("Leyendo factura..."):
        try:
            with pdfplumber.open(archivo_pdf) as pdf:
                # Extraemos todo el texto de la primera página
                texto_completo = pdf.pages[0].extract_text()
                
                # --- LÓGICA DE EXTRACCIÓN (Concepto) ---
                # Buscamos patrones típicos en las facturas de Farmasi
                # Nota: Estos patrones pueden variar según el diseño del PDF
                orden_no = re.search(r"Orden No:?\s*(\w+)", texto_completo)
                factura_no = re.search(r"Factura No:?\s*(\w+)", texto_completo)
                total = re.search(r"Total:?\s*([\d,.]+)", texto_completo)
                
                # --- RESULTADO EN PANTALLA (TARJETA VISUAL) ---
                st.subheader("🔍 Datos Detectados")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.text_input("Nº ORDEN", value=orden_no.group(1) if orden_no else "No detectado")
                    st.text_input("Nº FACTURA", value=factura_no.group(1) if factura_no else "No detectado")
                
                with col2:
                    st.text_input("TOTAL (€)", value=total.group(1) if total else "0.00")
                    st.date_input("FECHA FACTURA")

                # Mostramos el texto extraído por si queremos ver qué hay dentro
                with st.expander("Ver texto bruto del PDF"):
                    st.code(texto_completo)
                
                if st.button("🚀 Confirmar y Enviar a Google Sheets"):
                    st.success("Dato listo para ser guardado (Pendiente conexión de escritura)")

        except Exception as e:
            st.error(f"No se pudo leer el PDF: {e}")

# --- BOTÓN PARA VOLVER AL PANEL ---
if st.button("⬅️ Volver al Panel de Control"):
    st.switch_page("app.py") # Solo si usas multipágina

