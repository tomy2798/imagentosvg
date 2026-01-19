"""
Módulo de vista principal
Maneja la interfaz principal de carga y visualización de resultados
"""

import streamlit as st
import time
import base64
import io
from PIL import Image
from .styles import get_loading_animation, get_status_badge, get_info_box, get_zoom_controls


class MainView:
    """Gestiona la vista principal de la aplicación"""

    def __init__(self):
        """Inicializa la vista principal"""
        # Inicializar estado de sesión
        if 'processing_stage' not in st.session_state:
            st.session_state.processing_stage = None
        if 'show_preview' not in st.session_state:
            st.session_state.show_preview = False
        if 'selected_view' not in st.session_state:
            st.session_state.selected_view = 'original'

    def render_upload_section(self):
        """
        Renderiza la sección de carga de imagen con diseño mejorado

        Returns:
            uploaded_file: Archivo subido o None
        """
        st.markdown("""
            <div class="custom-card animate-in">
                <h3>📤 Subir Imagen</h3>
            </div>
        """, unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Arrastra una imagen o haz clic para seleccionar",
            type=["png", "jpg", "jpeg"],
            help="Sube una imagen para convertir a formato vectorial (SVG y DXF)",
            label_visibility="collapsed"
        )

        return uploaded_file

    def render_top_thumbnails(self, uploaded_file, results):
        """
        Renderiza la tira horizontal de miniaturas en la parte superior
        """
        if not uploaded_file:
            return
        
        # Columnas para los botones invisibles que actúan como click handlers
        col1, col2, col3 = st.columns(3)
        
        # Preparar imágenes para las cards
        
        # 1. Original
        img_str = ""
        try:
            uploaded_file.seek(0)
            image = Image.open(uploaded_file)
            image.thumbnail((200, 200), Image.Resampling.LANCZOS)
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            uploaded_file.seek(0)
        except:
            pass

        # 2. SVG
        svg_content = results.get('svg') if results else None
        
        # 3. DXF (usando SVG modificado como preview)
        dxf_preview = None
        if svg_content:
            dxf_preview = svg_content.replace('fill="black"', 'fill="none" stroke="#00ff41" stroke-width="2"')
            dxf_preview = dxf_preview.replace('stroke="black"', 'stroke="#00ff41"')
            if 'stroke=' not in dxf_preview:
                dxf_preview = dxf_preview.replace('<path ', '<path stroke="#00ff41" fill="none" stroke-width="2" ')

        # Renderizar botones
        with col1:
            selected = st.session_state.selected_view == 'original'
            css_class = "thumbnail-card selected" if selected else "thumbnail-card"
            
            if st.button("📷 Original", key="btn_original", use_container_width=True, type="primary" if selected else "secondary"):
                st.session_state.selected_view = 'original'
                st.rerun()
                
            # Preview visual (HTML estático debajo del botón)
            st.markdown(f"""
                <div class="{css_class}" style="margin-top: -10px; pointer-events: none;">
                    <div class="thumbnail-preview">
                        <img src="data:image/png;base64,{img_str}" />
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            selected = st.session_state.selected_view == 'svg'
            css_class = "thumbnail-card selected" if selected else "thumbnail-card"
            disabled = svg_content is None
            
            if st.button("📐 SVG", key="btn_svg", use_container_width=True, disabled=disabled, type="primary" if selected else "secondary"):
                st.session_state.selected_view = 'svg'
                st.rerun()

            # Wrap SVG in a container with proper sizing
            if svg_content:
                # Modify SVG to fit thumbnail size
                import re
                # Try to add width/height and ensure proper scaling
                if '<svg' in svg_content:
                    # Replace or add width/height attributes
                    svg_modified = re.sub(r'<svg\s+', '<svg width="120" height="120" style="max-width: 100%; max-height: 100%;" ', svg_content, count=1)
                    # Ensure viewBox exists for proper scaling
                    if 'viewBox' not in svg_modified:
                        svg_modified = re.sub(r'<svg\s+', '<svg viewBox="0 0 500 500" ', svg_modified, count=1)
                    preview_html = f'<div class="thumbnail-preview">{svg_modified}</div>'
                else:
                    preview_html = f'<div class="thumbnail-preview">{svg_content}</div>'
            else:
                preview_html = '<div class="thumbnail-preview" style="color: #666;">Waiting...</div>'
            
            st.markdown(f"""
                <div class="{css_class}" style="margin-top: -10px; pointer-events: none;">
                    {preview_html}
                </div>
            """, unsafe_allow_html=True)

        with col3:
            selected = st.session_state.selected_view == 'dxf'
            css_class = "thumbnail-card selected" if selected else "thumbnail-card"
            disabled = results is None or results.get('dxf') is None
            
            if st.button("🔧 DXF", key="btn_dxf", use_container_width=True, disabled=disabled, type="primary" if selected else "secondary"):
                st.session_state.selected_view = 'dxf'
                st.rerun()

            # Wrap DXF preview in a container with proper sizing
            if dxf_preview:
                # Modify SVG to fit thumbnail size
                import re
                if '<svg' in dxf_preview:
                    # Replace or add width/height attributes
                    dxf_modified = re.sub(r'<svg\s+', '<svg width="120" height="120" style="max-width: 100%; max-height: 100%;" ', dxf_preview, count=1)
                    # Ensure viewBox exists for proper scaling
                    if 'viewBox' not in dxf_modified:
                        dxf_modified = re.sub(r'<svg\s+', '<svg viewBox="0 0 500 500" ', dxf_modified, count=1)
                    preview_html = f'<div class="thumbnail-preview dark">{dxf_modified}</div>'
                else:
                    preview_html = f'<div class="thumbnail-preview dark">{dxf_preview}</div>'
            else:
                preview_html = '<div class="thumbnail-preview dark" style="color: #666;">Waiting...</div>'
            
            st.markdown(f"""
                <div class="{css_class}" style="margin-top: -10px; pointer-events: none;">
                    {preview_html}
                </div>
            """, unsafe_allow_html=True)

    def render_viewer_with_zoom(self, uploaded_file, results):
        """
        Renderiza un visualizador con controles de zoom integrados
        """
        import streamlit.components.v1 as components
        
        view = st.session_state.selected_view
        
        # Preparar contenido según la vista seleccionada
        content_html = ""
        content_type = None
        
        if view == 'original' and uploaded_file:
            # Imagen original
            uploaded_file.seek(0)
            image = Image.open(uploaded_file)
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            uploaded_file.seek(0)
            
            content_html = f'<img id="zoomable-content" src="data:image/png;base64,{img_str}" style="max-width: 100%; max-height: 100%; transition: transform 0.2s ease;">'
            content_type = 'image'
            
        elif view == 'svg' and results and results.get('svg'):
            # SVG
            svg_content = results['svg']
            content_html = f'<div id="zoomable-content" style="transition: transform 0.2s ease;">{svg_content}</div>'
            content_type = 'svg'
            
        elif view == 'dxf' and results and results.get('dxf'):
            # DXF preview (usando SVG modificado)
            svg_content = results.get('svg', '')
            if svg_content:
                dxf_preview = svg_content.replace('fill="black"', 'fill="none" stroke="#00ff41" stroke-width="2"')
                dxf_preview = dxf_preview.replace('stroke="black"', 'stroke="#00ff41"')
                if 'stroke=' not in dxf_preview:
                    dxf_preview = dxf_preview.replace('<path ', '<path stroke="#00ff41" fill="none" stroke-width="2" ')
                content_html = f'<div id="zoomable-content" style="transition: transform 0.2s ease;">{dxf_preview}</div>'
                content_type = 'dxf'
        
        # Si no hay contenido, no renderizar nada
        if not content_html:
            return
        
        # Determinar el fondo según el tipo
        bg_class = 'viewer-bg-dark' if content_type == 'dxf' else 'viewer-bg-light'
        
        # Títulos
        titles = {
            'original': '📷 Imagen Original',
            'svg': '📐 Vector SVG',
            'dxf': '🔧 Vista DXF'
        }
        
        # HTML completo con controles de zoom
        viewer_html = f'''
        <div style="background: #171717; border: 1px solid #262626; border-radius: 0.5rem; padding: 1.5rem; margin-top: 1rem;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #262626;">
                <div style="font-size: 1.1rem; font-weight: 600; color: #fafafa;">{titles.get(view, 'Vista')}</div>
            </div>
            
            <div id="viewer-container" class="{bg_class}" style="position: relative; height: 600px; overflow: hidden; border-radius: 0.5rem; display: flex; align-items: center; justify-content: center;">
                {content_html}
                
                <!-- Controles de Zoom -->
                <div style="position: absolute; bottom: 1rem; left: 50%; transform: translateX(-50%); display: flex; gap: 0.5rem; background: #171717; border: 1px solid #262626; border-radius: 0.5rem; padding: 0.5rem; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.4); z-index: 10;">
                    <button onclick="zoomOut()" style="background: #262626; border: 1px solid #262626; color: #fafafa; width: 32px; height: 32px; border-radius: 0.25rem; cursor: pointer; font-size: 16px; transition: all 0.2s;">−</button>
                    <button onclick="zoomReset()" style="background: #262626; border: 1px solid #262626; color: #fafafa; width: 32px; height: 32px; border-radius: 0.25rem; cursor: pointer; font-size: 16px; transition: all 0.2s;">⊙</button>
                    <button onclick="zoomIn()" style="background: #262626; border: 1px solid #262626; color: #fafafa; width: 32px; height: 32px; border-radius: 0.25rem; cursor: pointer; font-size: 16px; transition: all 0.2s;">+</button>
                    <button onclick="toggleFullscreen()" style="background: #262626; border: 1px solid #262626; color: #fafafa; width: 32px; height: 32px; border-radius: 0.25rem; cursor: pointer; font-size: 16px; transition: all 0.2s;">⛶</button>
                </div>
            </div>
        </div>
        
        <style>
            .viewer-bg-light {{
                background-image:
                    linear-gradient(45deg, #f0f0f0 25%, transparent 25%),
                    linear-gradient(-45deg, #f0f0f0 25%, transparent 25%),
                    linear-gradient(45deg, transparent 75%, #f0f0f0 75%),
                    linear-gradient(-45deg, transparent 75%, #f0f0f0 75%);
                background-size: 20px 20px;
                background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
                background-color: #ffffff;
            }}
            
            .viewer-bg-dark {{
                background: #000000;
            }}
            
            button:hover {{
                background: #404040 !important;
                border-color: #a1a1aa !important;
            }}
            
            button:active {{
                transform: scale(0.95);
            }}
        </style>
        
        <script>
            let currentZoom = 1;
            let isDragging = false;
            let startX, startY;
            let translateX = 0, translateY = 0;
            
            const content = document.getElementById('zoomable-content');
            const container = document.getElementById('viewer-container');
            
            function zoomIn() {{
                currentZoom = Math.min(currentZoom + 0.25, 5);
                updateTransform();
            }}
            
            function zoomOut() {{
                currentZoom = Math.max(currentZoom - 0.25, 0.5);
                updateTransform();
            }}
            
            function zoomReset() {{
                currentZoom = 1;
                translateX = 0;
                translateY = 0;
                updateTransform();
            }}
            
            function updateTransform() {{
                if (content) {{
                    content.style.transform = `translate(${{translateX}}px, ${{translateY}}px) scale(${{currentZoom}})`;
                }}
            }}
            
            function toggleFullscreen() {{
                if (!document.fullscreenElement) {{
                    container.requestFullscreen();
                }} else {{
                    document.exitFullscreen();
                }}
            }}
            
            // Pan con mouse drag
            container.addEventListener('mousedown', (e) => {{
                if (currentZoom > 1) {{
                    isDragging = true;
                    startX = e.clientX - translateX;
                    startY = e.clientY - translateY;
                    container.style.cursor = 'grabbing';
                }}
            }});
            
            container.addEventListener('mousemove', (e) => {{
                if (isDragging) {{
                    translateX = e.clientX - startX;
                    translateY = e.clientY - startY;
                    updateTransform();
                }}
            }});
            
            container.addEventListener('mouseup', () => {{
                isDragging = false;
                container.style.cursor = currentZoom > 1 ? 'grab' : 'default';
            }});
            
            container.addEventListener('mouseleave', () => {{
                isDragging = false;
                container.style.cursor = currentZoom > 1 ? 'grab' : 'default';
            }});
            
            // Zoom con rueda del mouse
            container.addEventListener('wheel', (e) => {{
                e.preventDefault();
                if (e.deltaY < 0) {{
                    zoomIn();
                }} else {{
                    zoomOut();
                }}
            }});
            
            // Actualizar cursor inicial
            container.style.cursor = currentZoom > 1 ? 'grab' : 'default';
        </script>
        '''
        
        components.html(viewer_html, height=720)
        
        # Botones de descarga si aplica
        if view == 'svg' and results and results.get('svg'):
            st.download_button(
                label="⬇️ Descargar SVG",
                data=results['svg'],
                file_name="vectorizado.svg",
                mime="image/svg+xml"
            )
        elif view == 'dxf' and results and results.get('dxf'):
            st.download_button(
                label="⬇️ Descargar DXF",
                data=results['dxf'],
                file_name="vectorizado.dxf",
                mime="application/dxf"
            )

    def render_main_viewer(self, uploaded_file, results, config):
        """
        Renderiza el visualizador principal según la selección
        """
        view = st.session_state.selected_view
        
        # Determinar qué contenido renderizar
        content_to_render = None
        
        if view == 'original' and uploaded_file:
            content_to_render = 'original'
        elif view == 'svg' and results and results.get('svg'):
            content_to_render = 'svg'
        elif view == 'dxf' and results and results.get('dxf'):
            content_to_render = 'dxf'
        
        # Early exit if no content - NO renderizar el contenedor vacío
        if content_to_render is None:
            return
        
        # Solo abrir el div si hay contenido para mostrar
        st.markdown('<div class="main-viewer animate-in">', unsafe_allow_html=True)
        
        # Header del viewer
        titles = {
            'original': '📷 Imagen Original',
            'svg': '📐 Vector SVG',
            'dxf': '🔧 Vista DXF'
        }
        
        st.markdown(f"""
            <div class="viewer-header">
                <div class="viewer-title">{titles.get(view, 'Vista')}</div>
            </div>
        """, unsafe_allow_html=True)

        # Renderizar el contenido correspondiente
        if content_to_render == 'original':
            self._render_original_image(uploaded_file)
        elif content_to_render == 'svg':
            self._render_svg_result(results['svg'])
        elif content_to_render == 'dxf':
            self._render_dxf_result(results['dxf'], results.get('svg'))

        st.markdown('</div>', unsafe_allow_html=True)

    def _render_original_image(self, uploaded_file):
        """Renderiza la imagen original con controles de zoom"""
        import streamlit.components.v1 as components
        
        uploaded_file.seek(0)
        image = Image.open(uploaded_file)
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        uploaded_file.seek(0)

        html = f'''
        <div class="preview-container" style="height: 600px;">
            <img id="main-image" src="data:image/png;base64,{img_str}" 
                 style="max-width: 100%; max-height: 100%; transition: transform 0.2s ease;">
            {get_zoom_controls()}
        </div>
        <script>
            // Re-bind zoom controls for this specific image
            document.getElementById('main-image').style.transform = 'scale(1)';
        </script>
        '''
        components.html(html, height=650)
        
        # Info del archivo
        file_size = len(uploaded_file.getvalue()) / 1024
        st.caption(f"Nombre: {uploaded_file.name} | Tamaño: {file_size:.2f} KB | Dimensiones: {image.size[0]}x{image.size[1]}px")

    def _render_svg_result(self, svg_content):
        """Renderiza el resultado SVG"""
        import streamlit.components.v1 as components
        
        html = f'''
        <div class="svg-preview" style="height: 600px;">
            {svg_content}
            {get_zoom_controls()}
        </div>
        '''
        components.html(html, height=650)
        
        # Botón de descarga
        st.download_button(
            label="⬇️ Descargar SVG",
            data=svg_content,
            file_name="vectorizado.svg",
            mime="image/svg+xml"
        )

    def _render_dxf_result(self, dxf_content, svg_content=None):
        """Renderiza el resultado DXF"""
        import streamlit.components.v1 as components
        
        # Usar SVG modificado como preview visual
        preview_content = ""
        if svg_content:
            svg_modified = svg_content.replace('fill="black"', 'fill="none" stroke="#00ff41" stroke-width="2"')
            svg_modified = svg_modified.replace('stroke="black"', 'stroke="#00ff41"')
            if 'stroke=' not in svg_modified:
                svg_modified = svg_modified.replace('<path ', '<path stroke="#00ff41" fill="none" stroke-width="2" ')
            preview_content = svg_modified

        html = f'''
        <div class="preview-dark-container" style="height: 600px;">
            <div class="preview-content" id="dxf-container">
                {preview_content}
            </div>
            {get_zoom_controls()}
        </div>
        '''
        components.html(html, height=650)
        
        st.download_button(
            label="⬇️ Descargar DXF",
            data=dxf_content,
            file_name="vectorizado.dxf",
            mime="application/dxf"
        )

    def show_processing_spinner(self, message="Procesando imagen..."):
        return st.spinner(message)

    def show_success(self, message):
        """Muestra mensaje de éxito con animación"""
        st.markdown(f"""
            <div class="animate-in" style="padding: 1rem; background: rgba(34, 197, 94, 0.15); border-left: 3px solid #22c55e; border-radius: 0.5rem; margin: 1rem 0; border: 1px solid rgba(34, 197, 94, 0.3);">
                <p style="margin: 0; color: #22c55e; font-weight: 500; font-size: 0.95rem;">✅ {message}</p>
            </div>
        """, unsafe_allow_html=True)

    def show_error(self, message):
        """Muestra mensaje de error con animación"""
        st.markdown(f"""
            <div class="animate-in" style="padding: 1rem; background: rgba(220, 38, 38, 0.15); border-left: 3px solid #dc2626; border-radius: 0.5rem; margin: 1rem 0; border: 1px solid rgba(220, 38, 38, 0.3);">
                <p style="margin: 0; color: #dc2626; font-weight: 500; font-size: 0.95rem;">❌ {message}</p>
            </div>
        """, unsafe_allow_html=True)
