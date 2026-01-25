import streamlit as st
import pandas as pd
from pyslope import Slope, Material

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================
st.set_page_config(page_title="Análisis Pyslope", layout="wide")

# Diccionario de traducción de colores
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
    st.title("⛰️ Análisis de Estabilidad (Control de Ejes)")

    # ==========================================
    # 2. ENTRADAS LATERALES
    # ==========================================
    with st.sidebar:
        st.header("1. Geometría")
        height = st.number_input("Altura Talud (m)", 1.0, 50.0, 6.0, step=0.5)
        angle = st.number_input("Ángulo (°)", 10.0, 89.0, 45.0, step=1.0)
        st.divider()
        st.header("2. Agua")
        nf_prof = st.number_input("Profundidad NF (m)", 0.0, 20.0, 3.0, step=0.5)
        
        st.divider()
        # --- SECCIÓN DE CONTROL GRÁFICO ---
        st.header("3. ⚙️ Configuración del Gráfico")
        
        # Dimensiones
        c1, c2 = st.columns(2)
        ancho_fig = c1.number_input("Ancho (px)", 300, 2000, 800, step=50)
        alto_fig = c2.number_input("Alto (px)", 300, 2000, 600, step=50)
        
        # Control de Ejes (Rangos)
        st.subheader("Límites de los Ejes")
        usar_limites = st.checkbox("Forzar límites manuales", value=False)
        
        if usar_limites:
            c3, c4 = st.columns(2)
            # VALORES INICIALES AJUSTADOS:
            # X: Empieza un poco antes del pie (-5) y termina después de la cresta (30)
            x_min = c3.number_input("X Mín (m)", value=0.0, step=1.0)
            x_max = c4.number_input("X Máx (m)", value=30.0, step=1.0)
            
            c5, c6 = st.columns(2)
            # Y: Empieza abajo (-10) para ver cimentación y termina arriba (15) para ver talud
            y_min = c5.number_input("Y Mín (m)", value=0.0, step=1.0)
            y_max = c6.number_input("Y Máx (m)", value=15.0, step=1.0)
        else:
            # Valores por defecto (se ignorarán, pero definimos variables)
            x_min, x_max = None, None
            y_min, y_max = None, None

    # ==========================================
    # 3. TABLA DE ESTRATOS
    # ==========================================
    with st.expander("📝 Editar Capas y Colores", expanded=True):
        df_base = pd.DataFrame([
            {"Material": "Relleno", "γ": 18.0, "c": 5.0, "φ": 28.0, "Fondo": 5.0, "Color": "Rojizo"},
            {"Material": "Arcilla", "γ": 20.0, "c": 25.0, "φ": 22.0, "Fondo": 12.0, "Color": "Amarillo arena"},
        ])
        
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
                    width="medium",
                    options=list(MAPA_COLORES.keys()),
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
            slope = Slope(height=height, angle=angle, length=None)
            mats = []
            
            for i, row in tabla.iterrows():
                color_tecnico = MAPA_COLORES.get(row["Color"], "lightgrey")
                mats.append(Material(
                    unit_weight=row["γ"], friction_angle=row["φ"], cohesion=row["c"],
                    depth_to_bottom=row["Fondo"], name=row["Material"],
                    color=color_tecnico
                ))
            
            slope.set_materials(*mats)
            slope.set_water_table(nf_prof)
            
            slope.analyse_slope()
            fos = slope.get_min_FOS()
            
            # --- GENERAR GRÁFICO PYSLOPE ---
            fig = slope.plot_critical()

            # ==========================================
            # 5. CONTROL DE EJES Y DIMENSIONES
            # ==========================================
            
            # 1. Limpieza básica
            fig.layout.annotations = [] 
            fig.layout.shapes = []      
            
            # 2. Aplicar dimensiones personalizadas
            fig.update_layout(
                title_text="Sección Transversal Controlada",
                width=ancho_fig,   
                height=alto_fig,   
                template="plotly_white",
                autosize=False     
            )
            
            # 3. Aplicar límites de ejes si el usuario activó la casilla
            if usar_limites:
                fig.update_xaxes(range=[x_min, x_max], title="Distancia (m)")
                fig.update_yaxes(range=[y_min, y_max], title="Elevación (m)")
                # Forzar escala 1:1
                fig.update_yaxes(scaleanchor="x", scaleratio=1)
            else:
                # Automático pero con escala 1:1
                fig.update_yaxes(scaleanchor="x", scaleratio=1, title="Elevación (m)")
                fig.update_xaxes(title="Distancia (m)")

            # Mostrar Resultados
            st.divider()
            st.markdown(f"## Factor de Seguridad: :blue[{fos:.3f}]")
            
            st.plotly_chart(fig, use_container_width=False)

        except Exception as e:
            st.error(f"Error interno: {e}")

if __name__ == "__main__":
    main()