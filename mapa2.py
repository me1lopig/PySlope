# Crear código Streamlit modificado con tamaño fijo y zoom controlado por ancho/alto
import streamlit as st

st.set_page_config(
    page_title="Google Maps Viewer - Tamaño Fijo",
    page_icon="🗺️",
    layout="centered"
)

st.title("🗺️ Google Maps Viewer - Tamaño Fijo con Zoom")
st.markdown("El mapa tiene tamaño fijo. Los valores de ancho y alto controlan el nivel de zoom.")

with st.sidebar:
    st.header("Configuración del Mapa")
    lat = st.text_input("Latitud", value="40.4168")
    lon = st.text_input("Longitud", value="-3.7038")
    
    st.markdown("### Control de Zoom")
    st.markdown("*Valores más altos = más zoom (más cerca)*")
    width = st.slider("Ancho para Zoom", min_value=200, max_value=2000, value=800, step=50)
    height = st.slider("Alto para Zoom", min_value=200, max_value=1500, value=600, step=50)
    
    st.markdown("### Ejemplos")
    st.markdown("- Madrid: 40.4168, -3.7038")
    st.markdown("- Barcelona: 41.3851, 2.1734") 
    st.markdown("- Nueva York: 40.7128, -74.0060")
    st.markdown("- París: 48.8566, 2.3522")

try:
    lat_f = float(lat)
    lon_f = float(lon)
    if not (-90 <= lat_f <= 90 and -180 <= lon_f <= 180):
        st.error("Las coordenadas están fuera de rango.")
    else:
        # Calcular zoom basado en ancho y alto
        zoom_level = max(1, min(20, int((width + height) / 100)))
        
        map_url = f"https://www.google.com/maps?q={lat},{lon}&z={zoom_level}&output=embed"
        
        # Mostrar información del zoom
        st.info(f"📍 Nivel de Zoom: **{zoom_level}** (basado en ancho: {width}px, alto: {height}px)")
        
        # Mapa con tamaño fijo
        st.markdown(
            f"""
            <div style="border:2px solid #e5e7eb; border-radius:8px; overflow:hidden; width:800px; height:600px; margin:auto;">
                <iframe src="{map_url}" width="800" height="600" style="border:0;" allowfullscreen="" loading="lazy"></iframe>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.success(f"Mostrando mapa en ({lat}, {lon}) con zoom nivel {zoom_level}")
        
        if st.button("🌐 Abrir en Google Maps"):
            st.markdown(f"[Abrir en Google Maps](https://www.google.com/maps?q={lat},{lon}&z={zoom_level})")
            
except ValueError:
    st.error("Por favor, ingresa valores numéricos válidos para latitud y longitud.")

st.markdown("""
---
**📋 Instrucciones:**
- El mapa tiene un **tamaño fijo de 800x600 píxeles**
- Los valores de **ancho y alto controlan el nivel de zoom**
- Valores más altos = más zoom (vista más cercana)
- Valores más bajos = menos zoom (vista más lejana)
- Ingresa coordenadas y ajusta los valores para cambiar el zoom
""")