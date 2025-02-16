# Effect of slices on results

import pyslope as sp


s = sp.Slope(height=3, angle=30, length=None)

m1 = sp.Material(20, 35, 0, 0.5)
m2 = sp.Material(20, 35, 0, 1)
m3 = sp.Material(18, 30, 0, 5)

s.set_materials(m1, m2, m3)



for r in range(2, 10):
    s.add_single_circular_plane(
        c_x=s.get_bottom_coordinates()[0],
        c_y=s.get_bottom_coordinates()[1] + 2.5,
        radius=r,
    )


s.update_analysis_options(slices=15)
s.analyse_slope()

print(f'Slices: {50}')
for a in s._search:
    print(f'radius: {a["radius"]}, FOS: {a["FOS"]}')