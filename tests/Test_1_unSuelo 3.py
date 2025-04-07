# Prueba de la libreria pyslope

import pyslope as psp
import numpy as np
import openpyxl


def main():

    # Creación de la hoja excel en la que volcar los datos
    wb = openpyxl.Workbook()
    hoja = wb.active
    hoja.append(["Altura [m]","Pendiente [º]","Peso Especifico [kN/m3]","Cohesión [kPa]", "fi [º]", "FS"])  

    # bucle de cálculo
    for altura in np.arange(2,16):
        for pendiente in np.arange(10,91):
            for pesoEspecifico in np.arange(14,21):
                for cohesionTerreno in np.arange(0,51):
                    for anguloRozamiento in np.arange(5,41):

                        altura=float(altura)
                        pendiente=float(pendiente)
                        pesoEspecifico=float(pesoEspecifico)
                        cohesionTerreno=float(cohesionTerreno)
                        anguloRozamiento=float(anguloRozamiento)

                        s = psp.Slope(height=altura, angle=pendiente, length=None)

                        psp.Slope.plot_boundary(s, material_table=True, legend=True)
        
                        # Características del material

                        m1 = psp.Material(
                            unit_weight=pesoEspecifico,
                            friction_angle=anguloRozamiento,
                            cohesion=cohesionTerreno,
                            depth_to_bottom=altura*2,
                            name="Unidad 1"
                        )   

                        # Asignación del material
                        s.set_materials(m1)

                        # Cálculo
                        # s.set_analysis_limits(s.get_top_coordinates()[0] - 10, s.get_bottom_coordinates()[0] + 10) # limits

                        s.update_analysis_options(
                            slices=50,
                            iterations=2500,
                            tolerance=0.005,
                            max_iterations=50
                        )

                        s.analyse_slope()

                    # guardado en excel de los resultados de los calculos de una matriz de datos
       
                        hoja.append([altura,pendiente,pesoEspecifico,cohesionTerreno,anguloRozamiento, s.get_min_FOS()])  

    # Guardar el archivo Excel  
    nombre_archivo = 'analisis_talud.xlsx'  
    wb.save(nombre_archivo)
    
if __name__ == "__main__":
    main()