"""
Módulo de configuración
Define configuraciones por defecto y constantes de la aplicación
"""

# Configuración de la página
PAGE_CONFIG = {
    'page_title': 'Image to Vector Converter',
    'page_icon': '🎨',
    'layout': 'wide'
}

# Configuración por defecto del preprocesador
DEFAULT_PREPROCESSOR_CONFIG = {
    'threshold_method': 'OTSU',
    'threshold_value': 127,
    'noise_reduction': True
}

# Configuración por defecto del vectorizador
DEFAULT_VECTORIZER_CONFIG = {
    'color_mode': 'binary',
    'filter_speckle': 4,
    'corner_threshold': 60,
    'length_threshold': 4.0,
    'mode': 'spline',
    'splice_threshold': 45,
    'path_precision': 8
}

# Configuración por defecto del convertidor DXF
DEFAULT_DXF_CONFIG = {
    'bezier_subdivisions': 30,
    'use_splines': True,
    'tolerance': 0.1
}

# Formatos de archivo soportados
SUPPORTED_IMAGE_FORMATS = ['png', 'jpg', 'jpeg']

# Mensajes de la aplicación
MESSAGES = {
    'processing': 'Procesando imagen...',
    'success': 'Procesamiento completado exitosamente',
    'upload_help': 'Sube una imagen para convertir a formato vectorial',
    'no_results': '👈 Sube una imagen y haz clic en \'Convertir a Vector\' para comenzar',
    'svg_ready': 'SVG generado exitosamente',
    'dxf_ready': 'Archivo DXF listo para CAD/CNC'
}

# Textos de ayuda
HELP_TEXTS = {
    'preprocessing': 'Mejora la calidad para imágenes con ruido o baja calidad',
    'threshold_otsu': 'OTSU es automático y funciona bien en la mayoría de casos',
    'color_mode': 'Binary para logos en blanco y negro, Color para imágenes con múltiples colores',
    'filter_speckle': 'Elimina puntos pequeños y ruido (valores más altos = más filtrado)',
    'corner_threshold': 'Sensibilidad para detectar esquinas (60-100 típico para logos)',
    'mode': 'Spline = curvas suaves (recomendado para DXF), Polygon = segmentos rectos',
    'bezier_subdivisions': 'Mayor número = curvas más suaves pero archivos más grandes',
    'use_splines': 'Usa splines DXF nativos para curvas más precisas (recomendado)',
    'tolerance': 'Tolerancia para conectar paths cercanos (valores pequeños = más preciso)'
}
