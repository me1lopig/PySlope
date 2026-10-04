import numpy as np

class GeoModel:
    def __init__(self, terrain_pts, layers, water_pts=None):
        """
        terrain_pts: array de shape (N, 2) con [x, y]
        layers: lista de diccionarios con {'top_pts': array(N,2), 'gamma': float, 'c': float, 'phi': float}
        water_pts: array de shape (N, 2) con [x, y] (opcional)
        """
        self.terrain = np.array(terrain_pts)
        self.layers = layers
        self.water = np.array(water_pts) if water_pts is not None else None
        
        # Pre-procesamiento de estratos garantizando compatibilidad topográfica
        for i, layer in enumerate(self.layers):
            if i == 0 or layer.get('top_pts') is None:
                # El estrato superior o único coincide con el terreno
                layer['top_interp'] = lambda x: np.interp(x, self.terrain[:,0], self.terrain[:,1])
            else:
                pts = np.array(layer['top_pts'])
                # Límite superior del estrato profundo (nunca superior al terreno natural)
                layer['top_interp'] = lambda x, p=pts: np.minimum(
                    np.interp(x, p[:,0], p[:,1]),
                    self.terrain_interp(x)
                )

    def terrain_interp(self, x):
        return np.interp(x, self.terrain[:,0], self.terrain[:,1])

    def water_interp(self, x):
        if self.water is None:
            return np.full_like(x, -np.inf)
        return np.interp(x, self.water[:,0], self.water[:,1])

    def get_slice_properties(self, x_mid, y_bot, y_top):
        n_slices = len(x_mid)
        c_eff = np.zeros(n_slices)
        phi_eff = np.zeros(n_slices)
        weight = np.zeros(n_slices)

        # De abajo hacia arriba para asignar propiedades del estrato correspondiente
        for i in range(len(self.layers)-1, -1, -1):
            layer = self.layers[i]
            layer_top = layer['top_interp'](x_mid)
            
            top_bound = np.minimum(layer_top, y_top)
            thickness = np.maximum(top_bound - y_bot, 0)
            
            weight += thickness * layer['gamma']
            
            mask_base_in_layer = (y_bot <= layer_top + 1e-4)
            mask_assign = mask_base_in_layer & (c_eff == 0) 
            
            c_eff[mask_assign] = layer['c']
            phi_eff[mask_assign] = layer['phi']

        return weight, c_eff, phi_eff
