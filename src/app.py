# Importar las librerías necesarias
#pip install pyslope plotly kaleido

from pyslope import Slope, Material

def main():
    # Crear un objeto Slope
    slope = Slope(height=5, angle=30, length=None)

    # Definir el primer material
    material1 = Material(
        unit_weight=20,      # Peso unitario en kN/m3
        friction_angle=30,   # Ángulo de fricción en grados
        cohesion=10,         # Cohesión en kPa
        depth_to_bottom=3,   # Profundidad desde la parte superior del talud hasta la base de la capa de material en metro
        name="Unidad 1"      # Denominación de la unidad
    )

    # Definir el segundo material
    material2 = Material(
        unit_weight=22,      # Peso unitario en kN/m3
        friction_angle=35,   # Ángulo de fricción en grados
        cohesion=15,         # Cohesión en kPa
        depth_to_bottom=6,   # Profundidad desde la parte superior del talud hasta la base de la capa de material en metros
        name="Unidad 2"      # Denominación de la unidad
    )

    # Asignar los materiales al talud
    slope.set_materials(material1, material2)

    # Definir el nivel freático
    slope.set_water_table(4)  # Profundidad del nivel freático desde la parte superior del talud en metros

    # Analizar el talud
    slope.analyse_slope()

    # Obtener el factor de seguridad mínimo
    min_fos = slope.get_min_FOS()
    print(f"El factor de seguridad mínimo es: {min_fos}")

    # Generar y guardar el gráfico del talud crítico
    fig = slope.plot_critical()
    fig.write_image("SalidaGrafica.png")

if __name__ == "__main__":
    main()
