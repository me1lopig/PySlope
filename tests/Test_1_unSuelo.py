# Carga de las librerías 

import pyslope as psp
import numpy as np
import openpyxl

# Función principal
def main():

    # Creación de la hoja excel en la que volcar los datos
    wb = openpyxl.Workbook()
    hoja = wb.active
    hoja.append(["Cohesión [kPa]", "fi [º]", "FS"]) # encabezados de los datos

    # bucle de cálculo con variacion de los patametros resistentes del terreno

    for cohesionTerreno in np.arange(5,101):
        for anguloRozamiento in np.arange(5,35):

            cohesionTerreno=float(cohesionTerreno)
            anguloRozamiento=float(anguloRozamiento)

            # Características geoemtricas del talud
            s = psp.Slope(height=15, angle=45, length=None)

            psp.Slope.plot_boundary(s, material_table=True, legend=True)
        
            # Características del material

            m1 = psp.Material(
                unit_weight=18,
                friction_angle=anguloRozamiento,
                cohesion=cohesionTerreno,
                depth_to_bottom=30,
                name="Unidad 1"
            )   

            # Asignación del material
            s.set_materials(m1)

            # Cálculo
            # s.set_analysis_limits(s.get_top_coordinates()[0] - 10, s.get_bottom_coordinates()[0] + 10) # limites

            s.update_analysis_options(
                slices=25,
                iterations=2500,
                tolerance=0.005,
                max_iterations=50
            )

            s.analyse_slope()

            # Salida de resultados
            #print("Cohesion [kPa]=",cohesionTerreno,"FSmin=",s.get_min_FOS())

            # guardado en excel de los resultados de los calculos de una matriz de datos
            hoja.append([cohesionTerreno,anguloRozamiento, s.get_min_FOS()])  


    # Guardar el archivo Excel  
    nombre_archivo = 'analisis_talud.xlsx'  
    wb.save(nombre_archivo)
    
if __name__ == "__main__":
    main()