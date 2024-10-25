# Effect of slices on results

import pyslope as sp


s = sp.Slope(height=1, angle=None, length=1)

m1 = sp.Material(20, 35, 0, 0.5)
m2 = sp.Material(20, 35, 0, 1)
m3 = sp.Material(18, 30, 0, 5)

s.set_materials(m1, m2, m3)



for r in range(2, 6):
    s.add_single_circular_plane(
        c_x=s.get_bottom_coordinates()[0],
        c_y=s.get_bottom_coordinates()[1] + 2.5,
        radius=r,
    )

slices = [10, 25, 50, 500, 2000]

for i in slices:

    s.update_analysis_options(slices=i)
    s.analyse_slope()

    print(f'Slices: {i}')
    for a in s._search:
        print(f'radius: {a["radius"]}, FOS: {a["FOS"]}')