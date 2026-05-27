import streamlit as st
import pandas as pd
from pyslope import Slope, Material

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================
st.set_page_config(page_title="Análisis Pyslope", layout="wide")

def main():
    st.title("⛰️ Análisis de Estabilidad (Gráfico Original Pyslope)")

    # ==========================================
    # 2. ENTRADAS
    # ==========================================
    with st.sidebar:
        st.header("Geometría")
        height = st.number_input("Altura Talud (m)", 1.0, 50.0, 6.0, step=0.5)
        angle = st.number_input("Ángulo (°)", 10.0, 89.0, 45.0, step=1.0)
        st.divider()
        st.header("Agua")
        nf_prof = st.number_input("Profundidad NF (m)", 0.0, 20.0, 3.0, step=0.5)

    with st.expander("📝 Editar Capas de Suelo", expanded=True):
        df_base = pd.DataFrame([
            {"Material": "Relleno", "γ": 18.0, "c": 5.0, "φ": 28.0, "Fondo": 5.0},
            {"Material": "Arcilla", "γ": 20.0, "c": 25.0, "φ": 22.0, "Fondo": 12.0},
        ])
        
        # Tabla simple para introducir datos
        tabla = st.data_editor(
            df_base, 
            num_rows="dynamic", 
            use_container_width=True,
            column_config={
                "γ": st.column_config.NumberColumn("γ (kN/m³)", format="%.1f"),
                "c": st.column_config.NumberColumn("c (kPa)", format="%.1f"),
                "φ": st.column_config.NumberColumn("φ (°)", format="%.1f"),
                "Fondo": st.column_config.NumberColumn("Prof. Base (m)", format="%.2f")
            }
        )

    # ==========================================
    # 3. CÁLCULO
    # ==========================================
    if st.button("Calcular Factor de Seguridad", type="primary"):
        if tabla.empty: st.error("Tabla vacía"); return
        
        try:
            # Configuración del Modelo
            slope = Slope(height=height, angle=angle, length=None)
            mats = []
            
            # Colores base de Pyslope para los materiales
            colores_base = ['purple', 'yellow', 'brown', 'green', 'orange']
            
            for i, row in tabla.iterrows():
                mats.append(Material(
                    unit_weight=row["γ"], friction_angle=row["φ"], cohesion=row["c"],
                    depth_to_bottom=row["Fondo"], name=row["Material"],
                    color=colores_base[i % len(colores_base)]
                ))
            
            slope.set_materials(*mats)
            slope.set_water_table(nf_prof)
            
            # Ejecutar Análisis
            slope.analyse_slope()
            fos = slope.get_min_FOS()
            
            # Generar gráfico original de la librería
            fig = slope.plot_critical()

            # ==========================================
            # 4. LIMPIEZA MÍNIMA (Sin cambiar líneas)
            # ==========================================
            # Solo quitamos la tabla interna (annotations) y el fondo gris (shapes)
            # para que se vea limpio, pero respetamos las líneas originales.
            fig.layout.annotations = [] 
            fig.layout.shapes = []      
            
            # Ajustamos escala 1:1 para que no se deforme
            fig.update_yaxes(scaleanchor="x", scaleratio=1, title="Elevación (m)")
            fig.update_xaxes(title="Distancia (m)")
            
            fig.update_layout(
                title_text="Sección Transversal",
                height=600,
                template="plotly_white"
            )

            # ==========================================
            # 5. MOSTRAR RESULTADOS
            # ==========================================
            st.divider()
            
            # Mostramos el FS
            st.markdown(f"### Factor de Seguridad: :blue[{fos:.3f}]")
            
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Error interno: {e}")

if __name__ == "__main__":
    main()