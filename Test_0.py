# Prueba della libreria pyslope

import pyslope as sp

s = sp.Slope(height=3, angle=30, length=None)

fig = s.plot_boundary()  # store a plot in local variable

fig.show()