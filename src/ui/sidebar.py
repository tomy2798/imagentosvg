"""
Módulo de la barra lateral de configuración
Maneja todos los controles y configuraciones de la UI
"""

import streamlit as st


class Sidebar:
    """Gestiona la barra lateral de configuración"""

    def __init__(self):
        """Inicializa la barra lateral"""
        self.use_preprocessing = True
        self.threshold_method = "OTSU"
        self.threshold_value = 127
        self.noise_reduction = True
        self.upscale_factor = 1.0
        self.color_mode = "binary"
        self.filter_speckle = 4
        self.corner_threshold = 60
        self.mode = "spline"
        self.length_threshold = 4.0
        self.splice_threshold = 45
        self.path_precision = 8
        self.color_precision = 6
        self.layer_difference = 16
        self.max_iterations = 10
        self.hierarchical = "stacked"
        self.bezier_subdivisions = 30
        self.use_splines = True
        self.tolerance = 0.1

    def render(self):
        """Renderiza la barra lateral y retorna la configuración"""
        # Header con diseño mejorado - tema oscuro
        st.sidebar.markdown("""
            <div style="text-align: center; padding: 1.5rem 0; margin-bottom: 1rem; border-bottom: 1px solid #262626;">
                <h2 style="color: #fafafa; margin: 0; font-size: 1.5rem; font-weight: 600;">⚙️ Configuración</h2>
                <p style="color: #a1a1aa; margin: 0.5rem 0 0 0; font-size: 0.875rem;">
                    Ajusta los parámetros de conversión
                </p>
            </div>
        """, unsafe_allow_html=True)

        st.sidebar.markdown("---")

        # Sección de preprocesamiento
        self._render_preprocessing_section()

        st.sidebar.markdown("---")

        # Sección de vectorización
        self._render_vectorization_section()

        st.sidebar.markdown("---")

        # Sección de DXF
        self._render_dxf_section()

        st.sidebar.markdown("---")

        # Presets rápidos
        self._render_presets_section()

        return self.get_config()

    def _render_preprocessing_section(self):
        """Renderiza controles de preprocesamiento"""
        st.sidebar.markdown("""
            <div style="color: #fafafa; font-weight: 600; font-size: 1rem; margin-bottom: 0.75rem;">
                🔧 Preprocesamiento
            </div>
        """, unsafe_allow_html=True)

        self.use_preprocessing = st.sidebar.checkbox(
            "✓ Activar preprocesamiento",
            value=True,
            help="Mejora la calidad para imágenes con ruido o baja calidad"
        )

        if self.use_preprocessing:
            st.sidebar.markdown("<div style='margin-left: 1rem;'>", unsafe_allow_html=True)
            
            self.upscale_factor = st.sidebar.slider(
                "📈 Mejora de calidad (upscaling)",
                1.0, 4.0, 1.0, 0.5,
                help="Aumenta la resolución de la imagen antes de procesar. Útil para imágenes pequeñas o de baja calidad. 1.0 = sin cambio, 2.0 = doble tamaño"
            )

            self.threshold_method = st.sidebar.selectbox(
                "Método de umbralización",
                ["OTSU", "Adaptivo", "Manual"],
                help="OTSU es automático y funciona bien en la mayoría de casos"
            )

            if self.threshold_method == "Manual":
                self.threshold_value = st.sidebar.slider(
                    "Valor de umbral", 0, 255, 127
                )

            self.noise_reduction = st.sidebar.checkbox(
                "Reducción de ruido", value=True
            )

            st.sidebar.markdown("</div>", unsafe_allow_html=True)

    def _render_vectorization_section(self):
        """Renderiza controles de vectorización"""
        st.sidebar.markdown("""
            <div style="color: #fafafa; font-weight: 600; font-size: 1rem; margin-bottom: 0.75rem;">
                🎨 Vectorización
            </div>
        """, unsafe_allow_html=True)

        self.color_mode = st.sidebar.selectbox(
            "Modo de color",
            ["binary", "color"],
            help="Binary para logos en blanco y negro, Color para imágenes con múltiples colores",
            index=0
        )

        self.filter_speckle = st.sidebar.slider(
            "🔍 Filtro de manchas",
            0, 10, 4,
            help="Elimina puntos pequeños y ruido (valores más altos = más filtrado)"
        )

        self.corner_threshold = st.sidebar.slider(
            "📐 Detección de esquinas",
            0, 180, 60,
            help="Sensibilidad para detectar esquinas (60-100 típico para logos)"
        )

        self.mode = st.sidebar.selectbox(
            "Tipo de curvas",
            ["spline", "polygon"],
            help="Spline = curvas suaves (recomendado para DXF), Polygon = segmentos rectos",
            index=0
        )
        
        # Configuración Avanzada (colapsable)
        with st.sidebar.expander("⚙️ Configuración Avanzada", expanded=False):
            self.length_threshold = st.slider(
                "📏 Longitud de segmentos",
                3.5, 10.0, 4.0, 0.1,
                help="Longitud máxima de segmentos. Valores más bajos = más detalle (mejor para texto)"
            )
            
            self.splice_threshold = st.slider(
                "🔗 Umbral de unión",
                0, 180, 45,
                help="Ángulo mínimo para unir splines. Valores más bajos = curvas más precisas"
            )
            
            self.path_precision = st.slider(
                "🎯 Precisión de coordenadas",
                0, 10, 8,
                help="Decimales en coordenadas SVG. Mayor precisión = mejor calidad (especialmente para texto)"
            )
            
            self.max_iterations = st.slider(
                "🔄 Iteraciones máximas",
                1, 20, 10,
                help="Iteraciones de algoritmos internos. Más iteraciones = mejor calidad pero más lento"
            )
        
        # Configuración de Color (solo visible en modo color)
        if self.color_mode == "color":
            with st.sidebar.expander("🎨 Configuración de Color", expanded=True):
                self.color_precision = st.slider(
                    "🌈 Precisión de color",
                    1, 8, 6,
                    help="Bits significativos por canal RGB. Mayor valor = colores más precisos"
                )
                
                self.layer_difference = st.slider(
                    "📊 Diferencia entre capas",
                    1, 255, 16,
                    help="Diferencia de color entre capas de gradiente. Valores más bajos = más capas"
                )
                
                self.hierarchical = st.selectbox(
                    "Estrategia de clustering",
                    ["stacked", "cutout"],
                    help="Stacked = capas apiladas (recomendado), Cutout = sin apilar"
                )

    def _render_dxf_section(self):
        """Renderiza controles de configuración DXF"""
        st.sidebar.markdown("""
            <div style="color: #fafafa; font-weight: 600; font-size: 1rem; margin-bottom: 0.75rem;">
                📐 Configuración DXF
            </div>
        """, unsafe_allow_html=True)

        self.use_splines = st.sidebar.checkbox(
            "✓ Usar splines DXF nativos",
            value=True,
            help="Usa splines DXF nativos para curvas más precisas (recomendado)"
        )

        self.bezier_subdivisions = st.sidebar.slider(
            "📊 Subdivisiones Bezier",
            10, 100, 30,
            help="Mayor número = curvas más suaves pero archivos más grandes"
        )

        self.tolerance = st.sidebar.number_input(
            "🎯 Tolerancia de conexión",
            min_value=0.01,
            max_value=1.0,
            value=0.1,
            step=0.01,
            help="Tolerancia para conectar paths cercanos (valores pequeños = más preciso)"
        )

    def _render_presets_section(self):
        """Renderiza sección de presets rápidos"""
        st.sidebar.markdown("""
            <div style="color: #fafafa; font-weight: 600; font-size: 1rem; margin-bottom: 0.75rem;">
                ⚡ Presets Rápidos
            </div>
        """, unsafe_allow_html=True)

        preset = st.sidebar.selectbox(
            "Selecciona un preset",
            ["Personalizado", "Logo de Alta Calidad", "Texto y Tipografía", "Dibujo Técnico", "Ilustración Artística"],
            help="Configuraciones predefinidas para casos de uso comunes"
        )

        if preset == "Logo de Alta Calidad":
            self._apply_logo_preset()
        elif preset == "Texto y Tipografía":
            self._apply_text_preset()
        elif preset == "Dibujo Técnico":
            self._apply_technical_preset()
        elif preset == "Ilustración Artística":
            self._apply_artistic_preset()

        st.sidebar.markdown("""
            <div style="margin-top: 1rem; padding: 0.75rem; background: #171717; border: 1px solid #262626; border-radius: 0.5rem;">
                <p style="margin: 0; color: #a1a1aa; font-size: 0.875rem; text-align: center;">
                    💡 Tip: Experimenta con diferentes configuraciones para mejores resultados
                </p>
            </div>
        """, unsafe_allow_html=True)

    def _apply_logo_preset(self):
        """Aplica preset optimizado para logos"""
        self.use_preprocessing = True
        self.threshold_method = "OTSU"
        self.noise_reduction = True
        self.color_mode = "binary"
        self.filter_speckle = 6
        self.corner_threshold = 80
        self.mode = "spline"
        self.bezier_subdivisions = 40
        self.use_splines = True
        self.tolerance = 0.05

    def _apply_technical_preset(self):
        """Aplica preset optimizado para dibujos técnicos"""
        self.use_preprocessing = True
        self.threshold_method = "OTSU"
        self.noise_reduction = True
        self.color_mode = "binary"
        self.filter_speckle = 2
        self.corner_threshold = 45
        self.mode = "polygon"
        self.bezier_subdivisions = 20
        self.use_splines = False
        self.tolerance = 0.01

    def _apply_artistic_preset(self):
        """Aplica preset optimizado para ilustraciones artísticas"""
        self.use_preprocessing = False
        self.color_mode = "color"
        self.filter_speckle = 8
        self.corner_threshold = 100
        self.mode = "spline"
        self.bezier_subdivisions = 50
        self.use_splines = True
        self.tolerance = 0.15
    
    def _apply_text_preset(self):
        """Aplica preset optimizado para texto y tipografía"""
        self.use_preprocessing = True
        self.upscale_factor = 2.0
        self.threshold_method = "OTSU"
        self.noise_reduction = True
        self.color_mode = "binary"
        self.filter_speckle = 3
        self.corner_threshold = 30
        self.mode = "spline"
        self.length_threshold = 3.5
        self.splice_threshold = 30
        self.path_precision = 10
        self.max_iterations = 15
        self.bezier_subdivisions = 50
        self.use_splines = True
        self.tolerance = 0.05

    def get_config(self):
        """
        Retorna la configuración actual como diccionarios separados

        Returns:
            dict: Configuración completa con claves preprocessor, vectorizer, dxf
        """
        return {
            'use_preprocessing': self.use_preprocessing,
            'preprocessor': {
                'threshold_method': self.threshold_method,
                'threshold_value': self.threshold_value,
                'noise_reduction': self.noise_reduction,
                'upscale_factor': self.upscale_factor if self.use_preprocessing else 1.0
            },
            'vectorizer': {
                'color_mode': self.color_mode,
                'filter_speckle': self.filter_speckle,
                'corner_threshold': self.corner_threshold,
                'mode': self.mode,
                'length_threshold': self.length_threshold,
                'splice_threshold': self.splice_threshold,
                'path_precision': self.path_precision,
                'color_precision': self.color_precision,
                'layer_difference': self.layer_difference,
                'max_iterations': self.max_iterations,
                'hierarchical': self.hierarchical
            },
            'dxf': {
                'bezier_subdivisions': self.bezier_subdivisions,
                'use_splines': self.use_splines,
                'tolerance': self.tolerance
            }
        }
