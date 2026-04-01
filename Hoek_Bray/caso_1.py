import numpy as np
from scipy.optimize import fsolve
from scipy.interpolate import interp1d

class CalculadorHoekBray:
    def __init__(self):
        # Coeficientes A, B, C de Li & Tham (1991) - Ábaco 1 (Seco)
        self.coef_abaco_1 = {
            10: (0.000, -0.220, 0.040),
            20: (0.000, -0.364, 0.130),
            30: (0.010, -0.450, 0.260),
            40: (0.025, -0.580, 0.420),
            50: (0.045, -0.720, 0.610),
            60: (0.070, -0.910, 0.850),
            70: (0.110, -1.150, 1.180),
            80: (0.170, -1.500, 1.650),
            90: (0.240, -1.950, 2.300)
        }

    def obtener_coeficientes(self, alfa):
        angulos = sorted(self.coef_abaco_1.keys())
        A_vals = [self.coef_abaco_1[ang][0] for ang in angulos]
        B_vals = [self.coef_abaco_1[ang][1] for ang in angulos]
        C_vals = [self.coef_abaco_1[ang][2] for ang in angulos]
        
        f_A = interp1d(angulos, A_vals, kind='quadratic', fill_value="extrapolate")
        f_B = interp1d(angulos, B_vals, kind='quadratic', fill_value="extrapolate")
        f_C = interp1d(angulos, C_vals, kind='quadratic', fill_value="extrapolate")
        return f_A(alfa), f_B(alfa), f_C(alfa)

    def calcular_fs(self, H, alfa, c, phi, gamma):
        A, B, C = self.obtener_coeficientes(alfa)
        tan_phi = np.tan(np.radians(phi))
        
        def ecuacion(fs):
            if fs <= 0.01: return 1e6 
            term_friccion = tan_phi / fs
            term_cohesion = c / (gamma * H * fs)
            return term_cohesion - (A * term_friccion**2 + B * term_friccion + C)
        
        return fsolve(ecuacion, x0=1.2)[0]

def main():
    calc = CalculadorHoekBray()
    print("\n" + "="*65)
    print("TESTEO AVANZADO: ÁBACO 1 (HOEK & BRAY)")
    print("="*65)

    try:
        H = float(input("Altura del talud (H) [m]: "))
        alfa = float(input("Ángulo del talud (Slope Angle) [°]: "))
        c = float(input("Cohesión (c) [kPa]: "))
        phi = float(input("Ángulo de fricción (φ) [°]: "))
        gamma = float(input("Peso específico (γ) [kN/m³]: "))

        # Cálculo del Factor de Seguridad
        fs = calc.calcular_fs(H, alfa, c, phi, gamma)
        
        # --- VALORES DE LOS EJES Y PARÁMETRO SOLICITADO ---
        tan_phi = np.tan(np.radians(phi))
        
        # Valor solicitado: c / (gamma * H * tan(phi))
        parametro_estabilidad = c / (gamma * H * tan_phi)
        
        # Coordenadas exactas en el gráfico (incluyendo F)
        eje_x_cohesion = c / (gamma * H * fs)
        eje_y_friccion = tan_phi / fs

        print("\n" + "-"*65)
        print("PARÁMETROS DE ENTRADA AL ÁBACO")
        print("-"*65)
        print(f"VALOR SOLICITADO c / (γ·H·tanφ): {round(parametro_estabilidad, 4)}")
        print(f"ÁNGULO DEL TALUD (Slope Angle):  {round(alfa, 1)}°")
        
        print("\n" + "-"*65)
        print("COORDENADAS DE SOLUCIÓN (Punto de equilibrio en el gráfico)")
        print("-"*65)
        print(f"EJE X (c / γ·H·F):  {round(eje_x_cohesion, 4)}")
        print(f"EJE Y (tanφ / F):   {round(eje_y_friccion, 4)}")
        print("-"*65)

        print(f"\n>>> RESULTADO FINAL: FACTOR DE SEGURIDAD (F) = {round(fs, 3)}")
        print("="*65)

    except Exception as e:
        print(f"\n[Error]: Datos inválidos. {e}")

if __name__ == "__main__":
    main()