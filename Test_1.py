# Prueba de la libreria pyslope

import pyslope as psp

s = psp.Slope(height=3, angle=30, length=None)

psp.Slope.plot_boundary(s, material_table=False, legend=False)

# Material defined with key word arguments
m1 = psp.Material(
    unit_weight=20,
    friction_angle=45,
    cohesion=2,
    depth_to_bottom=5,
)

# Material defined with positional arguments
m2 = psp.Material(20, 30, 2, 3)

# An unlimited number of materials can be assigned at one time
s.set_materials(m1, m2)


# analisys
s.set_analysis_limits(s.get_top_coordinates()[0] - 5, s.get_bottom_coordinates()[0] + 5) # limits

s.update_analysis_options(
    slices=50,
    iterations=2500,
    tolerance=0.005,
    max_iterations=50
)


#s.analyse_slope() # aqui se produce el error

#print(s.get_min_FOS())

#s.plot_boundary()  # plots only the boundary
#s.plot_critical()  # plots the boundary with the critical failure of the slope
#s.plot_all_planes(max_fos=1) # plots boundary with all slope failures below fos i (where i is number)

