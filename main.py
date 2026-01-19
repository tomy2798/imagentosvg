"""
Image to Vector Converter - Aplicación Principal
Convierte imágenes raster a formatos vectoriales (SVG, DXF)
"""

import streamlit as st
import time

from src.core.pipeline import ProcessingPipeline
from src.ui.sidebar import Sidebar
from src.ui.main_view import MainView
from src.ui.styles import get_custom_css
from src.utils.config import PAGE_CONFIG


def setup_page():
    """Configura la página de Streamlit"""
    st.set_page_config(**PAGE_CONFIG)

    # Aplicar CSS personalizado
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    # CSS adicional para el layout
    st.markdown("""
        <style>
        /* Layout de 3 columnas personalizado */
        .main .block-container {
            max-width: 100% !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
            padding-top: 1rem !important;
        }

        /* Ancho del sidebar nativo (configuraciones) */
        section[data-testid="stSidebar"] {
            width: 320px !important;
            min-width: 320px !important;
        }
        </style>
    """, unsafe_allow_html=True)


def main():
    """Función principal de la aplicación"""
    # Configurar página
    setup_page()

    # Inicializar estado de sesión
    if 'results' not in st.session_state:
        st.session_state.results = None
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'last_uploaded_file' not in st.session_state:
        st.session_state.last_uploaded_file = None
    if 'config' not in st.session_state:
        st.session_state.config = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False

    # Inicializar componentes de UI
    sidebar = Sidebar()
    main_view = MainView()

    # Renderizar barra lateral derecha (configuraciones)
    config = sidebar.render()

    # Header y Carga de archivo
    st.markdown('<h1 style="margin-bottom: 1rem;">🎨 Image to Vector</h1>', unsafe_allow_html=True)
    
    uploaded_file = main_view.render_upload_section()

    # Lógica de auto-procesamiento
    should_process = False
    
    # 1. Nuevo archivo subido
    if uploaded_file is not None:
        # Si es un archivo diferente al anterior o no tenemos resultados
        if (st.session_state.last_uploaded_file != uploaded_file) or (st.session_state.results is None):
            st.session_state.uploaded_file = uploaded_file
            st.session_state.last_uploaded_file = uploaded_file
            should_process = True
            # Resetear vista a original al subir nueva imagen
            st.session_state.selected_view = 'original'
    
    # 2. Cambio de configuración (Auto-procesamiento)
    if st.session_state.results is not None and config != st.session_state.config:
        should_process = True
        st.session_state.uploaded_file = uploaded_file # Asegurar que tenemos el archivo

    # Procesar imagen
    if should_process and st.session_state.uploaded_file is not None:
        st.session_state.processing = True
        
        # Inicializar pipeline con configuración
        pipeline = ProcessingPipeline(
            use_preprocessing=config['use_preprocessing'],
            preprocessor_config=config['preprocessor'],
            vectorizer_config=config['vectorizer'],
            dxf_config=config['dxf']
        )

        # Mostrar spinner
        with main_view.show_processing_spinner('🚀 Procesando imagen automáticamente...'):
            # Procesar imagen
            results, message = pipeline.process(st.session_state.uploaded_file)

        # Guardar resultados
        if results['svg'] is not None or results['dxf'] is not None:
            main_view.show_success(f"{message}")
            st.session_state.results = results
            st.session_state.config = config
            st.session_state.processing = False
            
            # Cambiar vista a SVG automáticamente si es la primera vez
            if st.session_state.selected_view == 'original':
                st.session_state.selected_view = 'svg'
            
            st.rerun()
        else:
            main_view.show_error(f"{message}")
            st.session_state.processing = False

    # Renderizar UI Principal
    if st.session_state.uploaded_file is not None:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 1. Miniaturas Superiores
        main_view.render_top_thumbnails(
            st.session_state.uploaded_file,
            st.session_state.results
        )
        
        # 2. Visualizador Principal con Zoom
        if not st.session_state.processing:
            main_view.render_viewer_with_zoom(
                st.session_state.uploaded_file,
                st.session_state.results
            )

    # Footer
    render_footer()


def render_footer():
    """Renderiza el pie de página"""
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style='text-align: center; padding: 2rem 0 1rem 0; color: #a1a1aa; background: transparent; border-top: 1px solid #262626; margin-top: 3rem;'>
            <p style='margin: 0.5rem 0; font-size: 0.875rem;'>
                <strong style='color: #fafafa;'>Tecnologías:</strong> Streamlit · VTracer · ezdxf · svgpathtools
            </p>
            <p style='margin: 1rem 0 0 0; font-size: 0.75rem; opacity: 0.6;'>
                Desarrollado con ❤️ para diseñadores y makers
            </p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
