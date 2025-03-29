# Prueba de la libreria pyslope

import pyslope as ps

def main():


    s = ps.Slope(height=15, angle=45, length=None)

    ps.Slope.plot_boundary(s, material_table=False, legend=False)

    # Material defined with key word arguments
    m1 = ps.Material(
        unit_weight=20,
        friction_angle=30,
        cohesion=10,
        depth_to_bottom=25,
        name="Terreno",
        color="green"
    )

    # An unlimited number of materials can be assigned at one time
    s.set_materials(m1)

    # analisys
    s.set_analysis_limits(s.get_top_coordinates()[0] - 15, s.get_bottom_coordinates()[0] + 15) # limits

    s.analyse_slope()

    fig = s.plot_boundary()  # store a plot in local variable
    fig.show()

    critical=s.plot_critical()  # plots the boundary with the critical failure of the slope
    critical.show()

    allPlanes=s.plot_all_planes(max_fos=1) # plots boundary with all slope failures below fos i (where i is number)
    allPlanes.show()

    print("FS=%.3f"%s.get_min_FOS())

if __name__ == "__main__":
    main()