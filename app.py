# Importar las librerías externas
import streamlit as st
from pyslope import Slope, Material
import plotly.graph_objects as go

def main():
    # Configuración de la página
    st.title("Análisis de Estabilidad de Taludes mediante el Método de Bishop Simplificado para uso académico")

    # Entradas para los parámetros del talud
    st.header("Parámetros del Talud")
    height = st.number_input("Altura del talud (m)", min_value=0.0, value=5.0)
    angle = st.number_input("Ángulo del talud (grados)", min_value=0.0, max_value=90.0, value=45.0)
    
    #Profundidad del nivel freático
    nivel_freatico = st.number_input("Profundidad del nf (m) desde coronación", min_value=0.0,max_value=height, value=height*0.5)

    # Entradas para los parámetros del suelo
    st.header("Parámetros del Suelo")
    unit_weight = st.number_input("Peso aparente (kN/m³)", min_value=0.0, value=20.0)
    friction_angle = st.number_input("Ángulo de fricción (grados)", min_value=0.0, max_value=90.0, value=30.0)
    cohesion = st.number_input("Cohesión (kPa)", min_value=0.0, value=10.0)
    depth_to_bottom = st.number_input("Espesor del suelo (m)", min_value=height*1.5, value=height*2)


    # Advertencia si la profundidad del suelo es menor que 1.5 veces la altura del talud
    if depth_to_bottom < 1.5 * height:
        st.warning("Advertencia: La profundidad del suelo debe ser al menos 1.5 veces la altura del talud para obtener resultados precisos.")

    # Botón para calcular
    if st.button("Calcular"):
        # Crear un objeto Slope
        slope = Slope(height=height, angle=angle, length=None)

        # Definir el material
        material = Material(
            unit_weight=unit_weight,
            friction_angle=friction_angle,
            cohesion=cohesion,
            depth_to_bottom=depth_to_bottom,
            name="UG-01",
            color='magenta'
        )

        # Asignar el material al talud
        slope.set_materials(material)

        # Asignar el nivel freático
        slope.set_water_table(nivel_freatico)  # Profundidad del nivel freático desde la cabeza del talud

        # Analizar el talud
        slope.analyse_slope()

        # Obtener el factor de seguridad mínimo
        min_fos = slope.get_min_FOS()
        #st.success(f"El factor de seguridad mínimo es: {min_fos}")
        st.success("El factor de seguridad mínimo es: %.3f"%(min_fos))

        # Generar el gráfico del talud crítico
        fig = slope.plot_critical()

        # Ajustar la escala del gráfico
        fig.update_layout(
            autosize=True,
            width=800,  # Ajusta el ancho de la figura
            height=600  # Ajusta la altura de la figura
        )

        # Mostrar el gráfico usando st.plotly_chart
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
