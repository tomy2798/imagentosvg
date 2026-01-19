"""
Módulo de sidebar izquierdo con miniaturas
Muestra vistas previas pequeñas de las imágenes (Original, SVG, DXF)
"""

import streamlit as st
import base64
import io
from PIL import Image


class ThumbnailSidebar:
    """Gestiona el sidebar izquierdo con miniaturas clickeables"""

    def __init__(self):
        """Inicializa el sidebar de miniaturas"""
        # Inicializar estado si no existe
        if 'selected_view' not in st.session_state:
            st.session_state.selected_view = 'original'

    def render(self, uploaded_file=None, results=None):
        """
        Renderiza el sidebar izquierdo con miniaturas

        Args:
            uploaded_file: Archivo de imagen subido
            results: Diccionario con resultados del procesamiento
        """
        import streamlit.components.v1 as components

        # Preparar miniaturas
        thumbnails_html = self._generate_thumbnails_html(uploaded_file, results)

        # Renderizar sidebar HTML
        components.html(thumbnails_html, height=800, scrolling=True)

        return st.session_state.selected_view

    def _generate_thumbnails_html(self, uploaded_file=None, results=None):
        """
        Genera el HTML para las miniaturas

        Args:
            uploaded_file: Archivo de imagen subido
            results: Diccionario con resultados del procesamiento

        Returns:
            str: HTML con las miniaturas
        """
        selected = st.session_state.selected_view

        # Preparar imagen original
        original_thumbnail = ""
        if uploaded_file:
            try:
                image = Image.open(uploaded_file)
                # Crear thumbnail
                image.thumbnail((200, 200), Image.Resampling.LANCZOS)
                buffered = io.BytesIO()
                image.save(buffered, format="PNG")
                img_str = base64.b64encode(buffered.getvalue()).decode()
                original_thumbnail = f'<img src="data:image/png;base64,{img_str}" style="width: 100%; height: auto;">'
                uploaded_file.seek(0)  # Reset file pointer
            except:
                original_thumbnail = '<div class="thumbnail-placeholder">📷</div>'
        else:
            original_thumbnail = '<div class="thumbnail-placeholder">📷</div>'

        # Preparar thumbnail SVG
        svg_thumbnail = ""
        if results and results.get('svg'):
            svg_content = results['svg']
            # Modificar SVG para que sea más pequeño
            svg_thumbnail = f'<div style="width: 100%; height: 120px; overflow: hidden; display: flex; align-items: center; justify-content: center;">{svg_content}</div>'
        else:
            svg_thumbnail = '<div class="thumbnail-placeholder">📐</div>'

        # Preparar thumbnail DXF (usar SVG como preview)
        dxf_thumbnail = ""
        if results and results.get('dxf') and results.get('svg'):
            svg_content = results['svg']
            # Modificar SVG para líneas verdes
            svg_modified = svg_content.replace('fill="black"', 'fill="none" stroke="#00ff41" stroke-width="2"')
            svg_modified = svg_modified.replace('stroke="black"', 'stroke="#00ff41"')
            if 'stroke=' not in svg_modified:
                svg_modified = svg_modified.replace('<path ', '<path stroke="#00ff41" fill="none" stroke-width="2" ')
            dxf_thumbnail = f'<div style="width: 100%; height: 120px; overflow: hidden; display: flex; align-items: center; justify-content: center; background: #000;">{svg_modified}</div>'
        else:
            dxf_thumbnail = '<div class="thumbnail-placeholder">🔧</div>'

        html = f"""
        <style>
            .thumbnail-sidebar {{
                background: #171717;
                height: 100vh;
                padding: 1rem;
                display: flex;
                flex-direction: column;
                gap: 1rem;
                overflow-y: auto;
            }}

            .thumbnail-header {{
                color: #fafafa;
                font-size: 0.875rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
                text-align: center;
                padding-bottom: 0.75rem;
                border-bottom: 1px solid #262626;
            }}

            .thumbnail-item {{
                background: #0a0a0a;
                border: 2px solid #262626;
                border-radius: 0.5rem;
                padding: 0.5rem;
                cursor: pointer;
                transition: all 0.2s ease;
                overflow: hidden;
            }}

            .thumbnail-item:hover {{
                border-color: #a1a1aa;
                transform: translateY(-2px);
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            }}

            .thumbnail-item.selected {{
                border-color: #fafafa;
                background: #262626;
                box-shadow: 0 0 0 2px rgba(250, 250, 250, 0.2);
            }}

            .thumbnail-label {{
                color: #a1a1aa;
                font-size: 0.75rem;
                font-weight: 500;
                text-align: center;
                margin-top: 0.5rem;
                margin-bottom: 0.25rem;
            }}

            .thumbnail-item.selected .thumbnail-label {{
                color: #fafafa;
                font-weight: 600;
            }}

            .thumbnail-content {{
                width: 100%;
                height: 120px;
                display: flex;
                align-items: center;
                justify-content: center;
                background: #ffffff;
                border-radius: 0.25rem;
                overflow: hidden;
                background-image:
                    linear-gradient(45deg, #f0f0f0 25%, transparent 25%),
                    linear-gradient(-45deg, #f0f0f0 25%, transparent 25%),
                    linear-gradient(45deg, transparent 75%, #f0f0f0 75%),
                    linear-gradient(-45deg, transparent 75%, #f0f0f0 75%);
                background-size: 10px 10px;
                background-position: 0 0, 0 5px, 5px -5px, -5px 0px;
            }}

            .thumbnail-content.dark {{
                background: #000000;
                background-image: none;
            }}

            .thumbnail-placeholder {{
                font-size: 3rem;
                color: #a1a1aa;
                opacity: 0.3;
            }}

            .thumbnail-disabled {{
                opacity: 0.4;
                cursor: not-allowed;
            }}

            .thumbnail-disabled:hover {{
                transform: none;
                border-color: #262626;
            }}
        </style>

        <div class="thumbnail-sidebar">
            <div class="thumbnail-header">
                📁 Vistas
            </div>

            <!-- Original Image -->
            <div class="thumbnail-item {'selected' if selected == 'original' else ''} {'' if uploaded_file else 'thumbnail-disabled'}"
                 onclick="selectView('original')"
                 id="thumb-original">
                <div class="thumbnail-content">
                    {original_thumbnail}
                </div>
                <div class="thumbnail-label">📷 Original</div>
            </div>

            <!-- SVG View -->
            <div class="thumbnail-item {'selected' if selected == 'svg' else ''} {'' if results and results.get('svg') else 'thumbnail-disabled'}"
                 onclick="selectView('svg')"
                 id="thumb-svg">
                <div class="thumbnail-content">
                    {svg_thumbnail}
                </div>
                <div class="thumbnail-label">📐 SVG</div>
            </div>

            <!-- DXF View -->
            <div class="thumbnail-item {'selected' if selected == 'dxf' else ''} {'' if results and results.get('dxf') else 'thumbnail-disabled'}"
                 onclick="selectView('dxf')"
                 id="thumb-dxf">
                <div class="thumbnail-content dark">
                    {dxf_thumbnail}
                </div>
                <div class="thumbnail-label">🔧 DXF</div>
            </div>
        </div>

        <script>
            function selectView(view) {{
                // Enviar mensaje a Streamlit (esto no funciona directamente con st.session_state)
                // Por ahora, solo cambiar visualmente
                document.querySelectorAll('.thumbnail-item').forEach(item => {{
                    item.classList.remove('selected');
                }});
                document.getElementById('thumb-' + view).classList.add('selected');

                // Guardar en localStorage para sincronización
                localStorage.setItem('selectedView', view);

                // Disparar evento personalizado para comunicación
                window.parent.postMessage({{type: 'viewChange', view: view}}, '*');
            }}

            // Sincronizar con selección inicial
            const initialView = localStorage.getItem('selectedView') || 'original';
            if (initialView !== 'original') {{
                selectView(initialView);
            }}
        </script>
        """

        return html
