import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from geom_utils import GeoModel
from solver_bishop import grid_search_bishop
from dxf_parser import parse_dxf_to_dataframes
from reporter import generate_report

st.set_page_config(page_title="Estabilidad de Taludes 2D", layout="wide")
st.title("Cálculo de estabilidad de taludes 2D")
st.markdown("**Método de Bishop simplificado · Vectorización con NumPy**")

if 'ground' not in st.session_state:
    st.session_state.ground = pd.DataFrame({'X (m)': [0.0, 20.0, 35.0, 55.0], 'Y (m)': [20.0, 20.0, 8.0, 8.0]})
if 'layers' not in st.session_state:
    st.session_state.layers = pd.DataFrame({'Nombre': ['Suelo (arcilla limosa)'], 'Gamma (kN/m3)': [18.0], 'c (kPa)': [10.0], 'phi (º)': [28.0], 'Color': ['#e7d3a1']})
if 'layers_geom' not in st.session_state:
    st.session_state.layers_geom = None
if 'water' not in st.session_state:
    st.session_state.water = pd.DataFrame({'X (m)': [0.0, 22.0, 38.0, 55.0], 'Y (m)': [12.0, 11.0, 6.0, 6.0]})
if 'loads' not in st.session_state:
    st.session_state.loads = pd.DataFrame({'X inicio (m)': [3.0], 'X fin (m)': [10.0], 'q (kPa)': [15.0]})

tab_geo, tab_mat, tab_water, tab_seismic, tab_calc = st.tabs(["Geometría", "Niveles", "Agua y cargas", "Sismo", "Análisis"])

with tab_geo:
    st.subheader("Superficie del terreno")
    with st.expander("ℹ️ Guía de formato para importar DXF"):
        st.markdown("""
        Polilíneas (`LWPOLYLINE` o `LINE`) organizadas estrictamente en capas:
        * **`TERRENO`**: Perfil topográfico superficial.
        * **`ESTRATO_X`** *(ej. ESTRATO_1)*: Límite superior de estratos profundos.
        * **`NIVEL_FREATICO`**: Cota piezométrica.
        *Aviso cinemático: No se admiten voladizos ni paredes 100% verticales.*
        """)

    uploaded_dxf = st.file_uploader("Importar geometría", type=['dxf'])
    if uploaded_dxf is not None and st.button("Procesar y Cargar DXF", type="primary"):
        try:
            parsed = parse_dxf_to_dataframes(uploaded_dxf)
            if 'ground' in parsed:
                st.session_state.ground = parsed['ground']
            if 'water' in parsed:
                st.session_state.water = parsed['water']
            if 'layers' in parsed:
                st.session_state.layers = pd.DataFrame(parsed['layers']).drop(columns=['top_pts'])
                st.session_state.layers_geom = parsed['layers']
            st.rerun() 
        except Exception as e:
            st.error(f"Error procesando CAD: {e}")
            
    st.session_state.ground = st.data_editor(st.session_state.ground, num_rows="dynamic", use_container_width=True)

with tab_mat:
    st.subheader("Niveles geotécnicos")
    st.session_state.layers = st.data_editor(st.session_state.layers, num_rows="dynamic", use_container_width=True)

with tab_water:
    use_water = st.toggle("Considerar nivel freático", value=True)
    if use_water:
        st.session_state.water = st.data_editor(st.session_state.water, num_rows="dynamic", use_container_width=True)
    st.subheader("Cargas repartidas")
    st.session_state.loads = st.data_editor(st.session_state.loads, num_rows="dynamic", use_container_width=True)

with tab_seismic:
    col1, col2 = st.columns(2)
    kh = col1.number_input("Aceleración horizontal kh (×g)", min_value=0.0, max_value=1.0, value=0.0, step=0.01)
    kv = col2.number_input("Aceleración vertical kv (×g)", min_value=-1.0, max_value=1.0, value=0.0, step=0.01)

with tab_calc:
    col1, col2, col3 = st.columns(3)
    n_slices = col1.number_input("Nº de dovelas", value=40)
    gxmin = col1.number_input("X centro mín", value=15.0)
    gxmax = col2.number_input("X centro máx", value=45.0)
    gymin = col1.number_input("Y centro mín", value=25.0)
    gymax = col2.number_input("Y centro máx", value=50.0)
    gnx = col3.number_input("Divisiones X", value=22, min_value=2)
    gny = col3.number_input("Divisiones Y", value=22, min_value=2)
    gnr = col3.number_input("Radios por centro", value=26, min_value=6)
    calc_button = st.button("Calcular talud crítico", type="primary", use_container_width=True)

# Render Plotly
fig = go.Figure()
gx, gy = st.session_state.ground['X (m)'].tolist(), st.session_state.ground['Y (m)'].tolist()

# Plot Stratigraphy if parsed from DXF
if st.session_state.layers_geom is not None:
    for layer in st.session_state.layers_geom:
        if layer['top_pts'] is not None:
            pts = layer['top_pts']
            fig.add_trace(go.Scatter(x=pts[:,0], y=pts[:,1], mode='lines', name=layer['Nombre'], line=dict(width=2)))
fig.add_trace(go.Scatter(x=gx, y=gy, mode='lines+markers', name='Terreno', line=dict(color='black', width=3), fill='tozeroy', fillcolor='rgba(231, 211, 161, 0.5)'))

if use_water and not st.session_state.water.empty:
    wx, wy = st.session_state.water['X (m)'].tolist(), st.session_state.water['Y (m)'].tolist()
    fig.add_trace(go.Scatter(x=wx, y=wy, mode='lines+markers', name='Nivel Freático', line=dict(color='blue', width=2, dash='dash')))

for idx, row in st.session_state.loads.iterrows():
    fig.add_trace(go.Scatter(x=[row['X inicio (m)'], row['X fin (m)']], y=[max(gy)+2, max(gy)+2], mode='lines', name=f"q={row['q (kPa)']} kPa", line=dict(color='purple', width=4)))

if calc_button:
    with st.spinner("Resolviendo matriz paramétrica..."):
        # Compilar modelo
        geom_layers = st.session_state.layers_geom if st.session_state.layers_geom else []
        if not geom_layers:
            # Construir diccionario de capas simples si no hay DXF
            props = st.session_state.layers.iloc[0]
            geom_layers.append({'top_pts': None, 'gamma': props['Gamma (kN/m3)'], 'c': props['c (kPa)'], 'phi': props['phi (º)']})
            
        water_arr = st.session_state.water[['X (m)', 'Y (m)']].values if use_water else None
        model = GeoModel(st.session_state.ground[['X (m)', 'Y (m)']].values, geom_layers, water_arr)
        
        # Malla de búsqueda
        x_c = np.linspace(gxmin, gxmax, gnx)
        y_c = np.linspace(gymin, gymax, gny)
        radii = np.linspace(2.0, (gymax - min(gy)) * 2, gnr)
        loads_list = st.session_state.loads.to_dict('records')
        
        # Solver
        fs_min, circle = grid_search_bishop(model, x_c, y_c, radii, loads_list, n_slices, kh=kh, kv=kv)
        
        if circle:
            xc, yc, r = circle
            fig.add_trace(go.Scatter(x=[xc], y=[yc], mode='markers', name='Centro Crítico', marker=dict(color='red', symbol='cross', size=10)))
            theta = np.linspace(np.pi, 2*np.pi, 100)
            fig.add_trace(go.Scatter(x=xc + r*np.cos(theta), y=yc + r*np.sin(theta), mode='lines', name=f'Rotura (FS={fs_min:.3f})', line=dict(color='red', width=2)))
            st.success(f"Cálculo completado. FS Mínimo: **{fs_min:.3f}** (Xc: {xc:.2f}, Yc: {yc:.2f}, R: {r:.2f})")
            
            fig.update_layout(height=600, xaxis_title="X (m)", yaxis_title="Elevación (m)", plot_bgcolor='rgba(242, 243, 246, 1)')
            fig.update_yaxes(scaleanchor="x", scaleratio=1)
            
            # Generar Reporte
            fig_bytes = fig.to_image(format="png", width=800, height=500, scale=2)
            st.session_state.report_buffer = generate_report(
                st.session_state.layers, st.session_state.water if use_water else pd.DataFrame(),
                st.session_state.loads, {'kh': kh, 'kv': kv},
                {'n_slices': n_slices, 'gnx': gnx, 'gny': gny, 'gnr': gnr},
                {'fs_min': fs_min, 'xc': xc, 'yc': yc, 'r': r}, fig_bytes
            )
        else:
            st.error("No se encontró una superficie de rotura cinemáticamente admisible.")

if 'report_buffer' not in st.session_state:
    fig.update_layout(height=600, xaxis_title="X (m)", yaxis_title="Elevación (m)", plot_bgcolor='rgba(242, 243, 246, 1)')
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
st.plotly_chart(fig, use_container_width=True)

if 'report_buffer' in st.session_state and st.session_state.report_buffer:
    st.download_button(label="⭳ Descargar Memoria de Cálculo (DOCX)", data=st.session_state.report_buffer, file_name="Estabilidad_Taludes.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
