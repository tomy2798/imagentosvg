# 🎨 Image to Vector Converter

Aplicación web que convierte imágenes raster (PNG, JPG) a formatos vectoriales (SVG, DXF) con líneas limpias y suaves, optimizada para aplicaciones CAD/CNC.

## ✨ Características

- 📤 **Carga de Imágenes**: Soporta PNG y JPG
- 🔧 **Preprocesamiento Avanzado**: Múltiples métodos de umbralización y reducción de ruido
- 🎨 **Vectorización de Alta Calidad**: Usa VTracer para conversión precisa
- 📐 **Exportación DXF**: Genera archivos DXF limpios sin escalones para CAD/CNC
- ⚙️ **Configuración Flexible**: Control total sobre parámetros de procesamiento
- 🖼️ **Visualizador Interactivo**: Vista en tiempo real con zoom y pan
- 👁️ **Tres Vistas**: Original, SVG y DXF con miniaturas clickeables
- ⬇️ **Descarga Rápida**: Botones de descarga integrados para SVG y DXF
- 🔄 **Reconversión Instantánea**: Aplica cambios de configuración al instante

## 🚀 Inicio Rápido

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación

1. Clona o descarga este repositorio

2. Crea y activa un entorno virtual (recomendado):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instala las dependencias:
```bash
pip install -r requirements.txt
```

### Ejecutar la Aplicación

```bash
streamlit run main.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
imagentosvg/
├── main.py                      # Aplicación principal de Streamlit
├── requirements.txt             # Dependencias de Python
├── README.md                    # Este archivo
├── CLAUDE.md                    # Guía para desarrollo con Claude Code
├── src/
│   ├── core/                    # Módulos de procesamiento central
│   │   ├── preprocessor.py      # Preprocesamiento de imágenes
│   │   ├── vectorizer.py        # Conversión imagen → SVG
│   │   ├── dxf_converter.py     # Conversión SVG → DXF
│   │   └── pipeline.py          # Pipeline completo de procesamiento
│   ├── ui/                      # Componentes de interfaz
│   │   ├── sidebar.py           # Sidebar derecho (configuraciones)
│   │   ├── thumbnail_sidebar.py # Sidebar izquierdo (miniaturas)
│   │   ├── viewer.py            # Visualizador central con zoom/pan
│   │   ├── main_view.py         # Componentes de vista principal
│   │   └── styles.py            # Estilos CSS personalizados
│   └── utils/                   # Utilidades
│       └── config.py            # Configuraciones y constantes
└── temp/                        # Archivos temporales (auto-generado)
```

## 🎯 Uso

### Interfaz de 3 Columnas

La aplicación cuenta con un diseño moderno inspirado en herramientas profesionales de diseño:

- **Sidebar Izquierdo**: Miniaturas clickeables de las 3 vistas (Original, SVG, DXF)
- **Visualizador Central**: Vista ampliada con controles de zoom y pan
- **Sidebar Derecho**: Panel de configuración con todos los parámetros

### Flujo de Trabajo

1. **Subir Imagen**: Usa el botón de carga en la parte superior
2. **Configurar Parámetros** (en el sidebar derecho):
   - **Preprocesamiento**: Activa para imágenes con ruido o baja calidad
   - **Vectorización**: Ajusta modo de color y detección de esquinas
   - **DXF**: Configura subdivisiones de curvas Bezier
3. **Convertir**: Haz clic en "🚀 Convertir a Vector"
4. **Visualizar**:
   - Haz clic en las miniaturas para cambiar de vista
   - Usa los controles de zoom (+/-) y pan (✋)
   - La rueda del mouse también funciona para zoom
5. **Descargar**: Usa los botones "⬇️ SVG" o "⬇️ DXF" en el header
6. **Reconvertir**: Si cambias la configuración, haz clic en "🔄 Reconvertir"

## ⚙️ Configuración Recomendada

### Para Logos y Diseños Simples

- **Modo de color**: Binary
- **Tipo de curvas**: Spline
- **Preprocesamiento**: Activado
- **Método de umbralización**: OTSU

### Para Imágenes con Múltiples Colores

- **Modo de color**: Color
- **Tipo de curvas**: Spline
- **Filtro de manchas**: 4-6

### Para Máxima Precisión en DXF

- **Subdivisiones Bezier**: 30-50
- **Modo de curvas**: Spline
- **Detección de esquinas**: 60-80

## 🛠️ Tecnologías

- **[Streamlit](https://streamlit.io/)**: Framework de aplicaciones web
- **[VTracer](https://github.com/visioncortex/vtracer)**: Motor de vectorización
- **[ezdxf](https://ezdxf.mozman.at/)**: Generación de archivos DXF
- **[svgpathtools](https://github.com/mathandy/svgpathtools)**: Procesamiento de paths SVG
- **[OpenCV](https://opencv.org/)**: Preprocesamiento de imágenes

## 📝 Notas Importantes

- Los archivos DXF generados están optimizados para **sin escalones** en las curvas
- El modo `spline` es esencial para obtener curvas suaves en DXF
- Mayor número de subdivisiones Bezier = archivos más grandes pero más suaves
- El preprocesamiento mejora significativamente los resultados en imágenes con ruido

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue primero para discutir cambios mayores.

## 📄 Licencia

Este proyecto está bajo la licencia MIT.

## 🙏 Agradecimientos

- VTracer por su excelente motor de vectorización
- La comunidad de Streamlit por el framework intuitivo
- ezdxf por hacer la generación de DXF tan simple
