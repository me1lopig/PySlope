# Prueba de la libreria pyslope

import pyslope as sp

s = sp.Slope(height=10, angle=30, length=None)


# Material defined with key word arguments
m1 = sp.Material(
    unit_weight=20,
    friction_angle=25,
    cohesion=20,
    depth_to_bottom=15
)


# An unlimited number of materials can be assigned at one time

s.set_materials(m1)

s.set_analysis_limits(s.get_top_coordinates()[0] - 5, s.get_bottom_coordinates()[0] + 5) # limits

s.analyse_slope()

print("FS=",s.get_min_FOS())