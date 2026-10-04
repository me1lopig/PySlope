import numpy as np

def get_slice_loads(x_mid, b, loads):
    q_total = np.zeros_like(x_mid)
    if loads:
        for load in loads:
            x1, x2 = min(load['X inicio (m)'], load['X fin (m)']), max(load['X inicio (m)'], load['X fin (m)'])
            mask = (x_mid >= x1) & (x_mid <= x2)
            q_total[mask] += load['q (kPa)']
    return q_total * b

def compute_FS_bishop(geo_model, xc, yc, R, loads=None, n_slices=40, gamma_w=9.81, kh=0.0, kv=0.0):
    x_terrain = geo_model.terrain[:, 0]
    x_min, x_max = x_terrain.min(), x_terrain.max()
    
    x_circ_min, x_circ_max = xc - R, xc + R
    x_eval = np.linspace(max(x_min, x_circ_min), min(x_max, x_circ_max), 500)
    
    y_terr = geo_model.terrain_interp(x_eval)
    y_circ = yc - np.sqrt(np.maximum(R**2 - (x_eval - xc)**2, 0))
    
    active_mask = y_terr > y_circ
    if not np.any(active_mask):
        return None
    
    valid_x = x_eval[active_mask]
    x_start, x_end = valid_x[0], valid_x[-1]
    
    if (x_end - x_start) < 0.05 * (x_max - x_min) or xc <= x_start or xc >= x_end:
        return None
        
    b = (x_end - x_start) / n_slices
    x_mid = np.linspace(x_start + b/2, x_end - b/2, n_slices)
    
    y_top = geo_model.terrain_interp(x_mid)
    y_bot = yc - np.sqrt(np.maximum(R**2 - (x_mid - xc)**2, 0))
    valid_slices = (y_top - y_bot) > 1e-4
    
    if not np.any(valid_slices):
        return None
        
    x_mid, y_top, y_bot = x_mid[valid_slices], y_top[valid_slices], y_bot[valid_slices]
    alpha = np.arcsin((x_mid - xc) / R)
    
    if np.max(np.abs(alpha)) > np.radians(60):
        return None
        
    weight_col, c_eff, phi_eff = geo_model.get_slice_properties(x_mid, y_bot, y_top)
    W = weight_col * b + get_slice_loads(x_mid, b, loads)
    
    y_water = geo_model.water_interp(x_mid)
    u = gamma_w * np.maximum(y_water - y_bot, 0)
    
    sin_alpha = np.sin(alpha)
    cos_alpha = np.cos(alpha)
    tan_phi = np.tan(np.radians(phi_eff))
    
    N_eff_initial = W * (1 - kv) - u * b
    N_eff = np.maximum(N_eff_initial, 0.0) # El suelo no resiste a tracción
    
    dir_slip = 1 if np.sum(W * sin_alpha) >= 0 else -1
    sin_alpha_dir = dir_slip * sin_alpha
    y_cg = (y_top + y_bot) / 2
    
    den = np.sum(W * (1 - kv) * sin_alpha_dir + kh * W * (yc - y_cg) / R)
    if den <= 0:
        return None
        
    FS = 1.0
    tol = 1e-4
    max_iter = 50
    
    for _ in range(max_iter):
        m_alpha = cos_alpha + (sin_alpha_dir * tan_phi) / FS
        if np.any(m_alpha < 0.2):
            return None # Bloqueo de divergencia numérica
            
        num = np.sum((c_eff * b + N_eff * tan_phi) / m_alpha)
        FS_new = num / den
        
        if not np.isfinite(FS_new) or FS_new <= 0.05:
            return None
        if np.abs(FS_new - FS) < tol:
            return FS_new
        FS = FS_new

    return None

def grid_search_bishop(geo_model, x_centers, y_centers, radii, loads=None, n_slices=40, kh=0.0, kv=0.0):
    fs_min = np.inf
    crit_circle = None
    
    for xc in x_centers:
        for yc in y_centers:
            for R in radii:
                fs = compute_FS_bishop(geo_model, xc, yc, R, loads, n_slices, 9.81, kh, kv)
                if fs is not None and fs < fs_min:
                    fs_min = fs
                    crit_circle = (xc, yc, R)
                    
    return fs_min, crit_circle
