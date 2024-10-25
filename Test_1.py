# Prueba della libreria pyslope

import pyslope as sp

s = sp.Slope(height=3, angle=30, length=None)

sp.Slope.plot_boundary(s, material_table=False, legend=False)

# Material defined with key word arguments
m1 = sp.Material(
    unit_weight=20,
    friction_angle=45,
    cohesion=2,
    depth_to_bottom=2
)

# Material defined with positional arguments
m2 = sp.Material(20, 30, 2, 5)

# An unlimited number of materials can be assigned at one time
s.set_materials(m1, m2)


# analisys
s.set_analysis_limits(s.get_top_coordinates()[0] - 5, s.get_bottom_coordinates()[0] + 5)