import streamlit as st
import pandas as pd
from pyslope import Slope, Material

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================
st.set_page_config(page_title="Análisis Pyslope", layout="wide")

# Diccionario de traducción: "Nombre en Español" -> "Nombre Técnico (Inglés)"
MAPA_COLORES = {
    "Marrón claro": "tan",
    "Amarillo arena": "khaki",
    "Marrón tierra": "peru",
    "Marrón oscuro": "saddlebrown",
    "Gris claro": "lightgrey",
    "Gris oscuro": "darkgrey",
    "Lila arcilla": "plum",
    "Verde claro": "lightgreen",
    "Azul claro": "lightblue",
    "Rojizo": "salmon",
    "Amarillo oro": "gold",
    "Púrpura": "purple"
}

def main():
    st.title("⛰️ Análisis de Estabilidad (Colores en Español)")

    # ==========================================
    # 2. ENTRADAS LATERALES
    # ==========================================
    with st.sidebar:
        st.header("Geometría")
        height = st.number_input("Altura Talud (m)", 1.0, 50.0, 6.0, step=0.5)
        angle = st.number_input("Ángulo (°)", 10.0, 89.0, 45.0, step=1.0)
        st.divider()
        st.header("Agua")
        nf_prof = st.number_input("Profundidad NF (m)", 0.0, 20.0, 3.0, step=0.5)

    # ==========================================
    # 3. TABLA DE ESTRATOS
    # ==========================================
    with st.expander("📝 Editar Capas y Colores", expanded=True):
        
        # DataFrame inicial con valores por defecto en ESPAÑOL (claves del diccionario)
        df_base = pd.DataFrame([
            {"Material": "Relleno", "γ": 18.0, "c": 5.0, "φ": 18.0, "Fondo": 5.0, "Color": "Rojizo"},
            {"Material": "Arcilla", "γ": 20.0, "c": 25.0, "φ": 20.0, "Fondo": 12.0, "Color": "Amarillo arena"},
        ])
        
        # Configuración del editor
        tabla = st.data_editor(
            df_base, 
            num_rows="dynamic", 
            use_container_width=True,
            column_config={
                "γ": st.column_config.NumberColumn("γ (kN/m³)", format="%.1f"),
                "c": st.column_config.NumberColumn("c (kPa)", format="%.1f"),
                "φ": st.column_config.NumberColumn("φ (°)", format="%.1f"),
                "Fondo": st.column_config.NumberColumn("Prof. Base (m)", format="%.2f"),
                "Color": st.column_config.SelectboxColumn(
                    "Color Visual",
                    help="Elige el color para la representación gráfica",
                    width="medium",
                    options=list(MAPA_COLORES.keys()), # Mostramos las claves en español
                    required=True
                )
            }
        )

    # ==========================================
    # 4. CÁLCULO
    # ==========================================
    if st.button("Calcular Factor de Seguridad", type="primary"):
        if tabla.empty: st.error("Tabla vacía"); return
        
        try:
            # Configurar Pyslope
            slope = Slope(height=height, angle=angle, length=None)
            mats = []
            
            for i, row in tabla.iterrows():
                # TRUCO: Buscamos el nombre español en el diccionario para obtener el inglés
                nombre_espanol = row["Color"]
                color_tecnico = MAPA_COLORES.get(nombre_espanol, "lightgrey") # lightgrey por si falla
                
                mats.append(Material(
                    unit_weight=row["γ"], 
                    friction_angle=row["φ"], 
                    cohesion=row["c"],
                    depth_to_bottom=row["Fondo"], 
                    name=row["Material"],
                    color=color_tecnico  # <--- Usamos el valor traducido
                ))
            
            slope.set_materials(*mats)
            slope.set_water_table(nf_prof)
            
            # Ejecutar Análisis
            slope.analyse_slope()
            fos = slope.get_min_FOS()
            
            # Generar gráfico original
            fig = slope.plot_critical()

            # ==========================================
            # 5. LIMPIEZA Y VISUALIZACIÓN
            # ==========================================
            # Limpieza visual estándar
            fig.layout.annotations = [] 
            fig.layout.shapes = []      
            
            # Ajustes de escala
            fig.update_yaxes(scaleanchor="x", scaleratio=1, title="Elevación (m)")
            fig.update_xaxes(title="Distancia (m)")
            
            fig.update_layout(
                title_text="Sección Transversal",
                height=600,
                template="plotly_white"
            )

            # Mostrar Resultados
            st.divider()
            st.markdown(f"### Factor de Seguridad: :blue[{fos:.3f}]")
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error interno: {e}")

if __name__ == "__main__":
    main()