import ezdxf
import pandas as pd
import numpy as np

def extract_polyline_from_layer(msp, layer_name):
    vertices = []
    for entity in msp.query(f'*[layer=="{layer_name}"]'):
        if entity.dxftype() == 'LWPOLYLINE':
            with entity.points() as pts:
                for pt in pts:
                    vertices.append([pt[0], pt[1]])
        elif entity.dxftype() == 'LINE':
            vertices.append([entity.dxf.start[0], entity.dxf.start[1]])
            vertices.append([entity.dxf.end[0], entity.dxf.end[1]])
            
    if not vertices:
        return None
        
    vertices = np.array(vertices)
    vertices = np.unique(vertices, axis=0) 
    vertices = vertices[vertices[:, 0].argsort()]
    
    return vertices

def parse_dxf_to_dataframes(dxf_stream):
    try:
        doc = ezdxf.read(dxf_stream)
        msp = doc.modelspace()
    except Exception as e:
        raise ValueError(f"Error al leer el archivo DXF: {e}")

    parsed_data = {}

    terrain_pts = extract_polyline_from_layer(msp, "TERRENO")
    if terrain_pts is not None:
        parsed_data['ground'] = pd.DataFrame(terrain_pts, columns=['X (m)', 'Y (m)'])

    water_pts = extract_polyline_from_layer(msp, "NIVEL_FREATICO")
    if water_pts is not None:
        parsed_data['water'] = pd.DataFrame(water_pts, columns=['X (m)', 'Y (m)'])

    layer_names = [layer.dxf.name for layer in doc.layers if layer.dxf.name.startswith("ESTRATO_")]
    layer_names.sort()
    
    strata_data = []
    if terrain_pts is not None:
        strata_data.append({'Nombre': 'Suelo Superficial (Auto)', 'Gamma (kN/m3)': 18.0, 'c (kPa)': 10.0, 'phi (º)': 28.0, 'Color': '#e7d3a1', 'top_pts': None})

    for lname in layer_names:
        pts = extract_polyline_from_layer(msp, lname)
        if pts is not None:
            strata_data.append({'Nombre': f'Material_{lname}', 'Gamma (kN/m3)': 20.0, 'c (kPa)': 20.0, 'phi (º)': 30.0, 'Color': '#b7d3b0', 'top_pts': pts})
            
    if strata_data:
        parsed_data['layers'] = strata_data

    return parsed_data
