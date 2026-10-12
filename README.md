# ⛰️ PySlope

> Análisis de estabilidad de taludes con Python, Streamlit y PySlope

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Status](https://img.shields.io/badge/status-Experimental-orange.svg)]()

---

## 📌 Descripción

PySlope es un repositorio orientado a la evaluación geotécnica de taludes mediante el método de Bishop simplificado, desarrollado en Python. El proyecto combina la librería `pyslope` con interfaces interactivas en `Streamlit` para permitir cálculos, análisis paramétricos y generación de informes técnicos en entornos de estudio y prueba.

El repositorio reúne varios prototipos y pruebas de concepto relacionados con:

- Análisis de estabilidad de taludes
- Evaluación por capas estratigráficas
- Variación de parámetros geométricos e hidráulicos
- Generación de reportes y documentos Word
- Visualización de resultados mediante gráficos interactivos

---

## 🧭 Objetivo del Proyecto

El objetivo principal es facilitar la evaluación de la estabilidad de taludes mediante herramientas accesibles, visuales y automatizadas, apoyando la validación técnica con escenarios múltiples y comparaciones entre condiciones de diseño.

Se usa principalmente para:

- Pruebas académicas
- Análisis técnico preliminar
- Modelación paramétrica de taludes
- Generación de documentación técnica con resultados reproducibles

---

## 🏗️ Estructura del Repositorio

```text
PySlope/
├── 📁 .devcontainer/              # Configuración del entorno de desarrollo
├── 📁 Hoek_Bray/                  # Ejemplos y pruebas con enfoque Hoek-Brown
│   └── caso_1.py
├── 📁 Streamlit/                  # Variantes de apps Streamlit
│   ├── app.py
│   ├── app_2.py
│   ├── app_3.py
│   ├── app_4.py
│   ├── app_5.py
│   ├── app_6.py
│   ├── app_7.py
│   └── app_8.py
├── 📁 variante_1/                 # Implementación alternativa con DXF
│   ├── app.py
│   ├── dxf_parser.py
│   ├── geom_utils.py
│   ├── solver_bishop.py
│   ├── reporter.py
│   ├── requirements.txt
│   └── lesen.txt
├── 📁 calculado/                 # Archivos de cálculo y resultados
├── 📁 docs/                      # Documentación del proyecto
├── 📄 README.md                  # Documentación general
├── 📄 LICENSE                    # Licencia Apache 2.0
├── 📄 requirements.txt           # Dependencias base
├── 📄 app_10.py                  # Aplicación principal de cálculo
├── 📄 app_provisionales.py       # Simulación multiescenario
├── 📄 mapa2.py                   # Visualizador de mapa con Google Maps
├── 📄 nf.py                      # Nivel freático / ejemplo auxiliar
├── 📄 documentacion.txt          # Referencia documental
└── 📄 .gitignore                 # Archivos ignorados por Git
```

---

## ⚙️ Tecnologías Utilizadas

- Python 3.8+
- Streamlit
- Pandas
- NumPy
- Plotly
- python-docx
- PySlope
- ezdxf (en variante_1)
- Kaleido (para exportación estática de gráficos)

---

## 🚀 Instalación

Clona el repositorio:

```bash
git clone https://github.com/me1lopig/PySlope.git
cd PySlope
```

Crea un entorno virtual e instala las dependencias:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
# o en Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Si deseas usar la variante con DXF y utilidades avanzadas:

```bash
pip install -r variante_1/requirements.txt
```

---

## ▶️ Cómo Ejecutar

### Aplicación principal

```bash
streamlit run app_10.py
```

### Análisis paramétrico y multiescenario

```bash
streamlit run app_provisionales.py
```

### Variante con DXF

```bash
streamlit run variante_1/app.py
```

### Mapa de referencia

```bash
streamlit run mapa2.py
```

---

## 📊 Funcionalidades Principales

### 1. Cálculo de estabilidad de taludes
El proyecto permite definir:

- altura del talud
- ángulo de inclinación
- nivel freático
- estratigrafía
- propiedades físicas del suelo

Posteriormente calcula el factor de seguridad mediante la librería `pyslope`.

### 2. Simulación multiescenario
La app `app_provisionales.py` permite estudiar rangos de variación para:

- altura del talud
- inclinación del talud
- nivel freático

Generando una matriz de resultados con estados como:

- Estable
- Crítico
- Inestable

### 3. Visualización gráfica
Se incluyen gráficos con `Plotly` y `Matplotlib` para mostrar:

- perfiles transversales del talud
- curvas de sensibilidad
- comportamiento ante cambios del nivel freático

### 4. Emisión de reportes
Se genera documentación Word con tablas, cifras y gráficos para presentar análisis de forma técnica.

---

## 🧪 Ejemplo Conceptual

El proyecto fue orientado a validar la estabilidad de taludes bajo distintas condiciones, comparando resultados con herramientas de referencia como GeoStudio. La documentación interna del repositorio indica que se está haciendo prueba con Geostudio 2002 y desarrollo de una interfaz tipo web para análisis geotécnico.

---

## 📁 Archivos Relevantes

- `app_10.py`: aplicación principal de análisis con interfaz Streamlit.
- `app_provisionales.py`: versión con análisis paramétrico y generación de memoria técnica.
- `Streamlit/`: versiones de prueba y evolución de la aplicación web.
- `variante_1/`: implementación alternativa con carga y cálculo más complejo.
- `documentacion.txt`: referencia de documentación rápida del proyecto.

---

## 📘 Licencia

Este proyecto está bajo la licencia Apache License 2.0. Consulta [LICENSE](LICENSE) para más detalles.

---

## 🤝 Contribución

Las contribuciones son bienvenidas. Para colaborar:

```bash
git checkout -b feature/nueva-funcionalidad
git commit -am "Añadir nueva funcionalidad"
git push origin feature/nueva-funcionalidad
```

---

## 🧑‍💻 Autor

- GitHub: [me1lopig](https://github.com/me1lopig)
- Repositorio: [PySlope](https://github.com/me1lopig/PySlope)

---

## ⚠️ Nota

Este repositorio está enfocado a desarrollo experimental y pruebas técnicas. Los resultados deben validarse con criterio profesional y, si se emplean en proyectos reales, deben verificarse con métodos de cálculo y revisión geo-técnica adecuados.

---

<p align="center">
  <strong>⭐ Gracias por visitar PySlope ⭐</strong>
</p>
