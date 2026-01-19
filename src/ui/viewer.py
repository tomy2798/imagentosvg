"""
Módulo de visualizador central
Muestra la imagen seleccionada con controles de zoom y pan
"""

import streamlit as st
import streamlit.components.v1 as components
import base64
import io
from PIL import Image


class ImageViewer:
    """Gestiona el visualizador central con zoom y pan"""

    def __init__(self):
        """Inicializa el visualizador"""
        pass

    def render(self, uploaded_file=None, results=None, selected_view='original'):
        """
        Renderiza el visualizador central con la imagen seleccionada

        Args:
            uploaded_file: Archivo de imagen subido
            results: Diccionario con resultados del procesamiento
            selected_view: Vista seleccionada ('original', 'svg', 'dxf')
        """
        if selected_view == 'original' and uploaded_file:
            self._render_original_view(uploaded_file)
        elif selected_view == 'svg' and results and results.get('svg'):
            self._render_svg_view(results['svg'])
        elif selected_view == 'dxf' and results and results.get('dxf'):
            self._render_dxf_view(results['svg'])  # Usar SVG como preview visual
        else:
            self._render_empty_view()

    def _render_original_view(self, uploaded_file):
        """Renderiza la vista de la imagen original con zoom y pan"""
        try:
            image = Image.open(uploaded_file)
            buffered = io.BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            uploaded_file.seek(0)  # Reset file pointer

            viewer_html = f"""
            <style>
                .viewer-container {{
                    width: 100%;
                    height: 80vh;
                    background: #000000;
                    border: 1px solid #262626;
                    border-radius: 0.5rem;
                    position: relative;
                    overflow: hidden;
                    display: flex;
                    flex-direction: column;
                }}

                .viewer-header {{
                    background: #171717;
                    border-bottom: 1px solid #262626;
                    padding: 0.75rem 1.25rem;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    color: #fafafa;
                    font-weight: 500;
                    font-size: 0.95rem;
                    z-index: 10;
                }}

                .viewer-content {{
                    flex: 1;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    overflow: hidden;
                    position: relative;
                    background-image:
                        linear-gradient(45deg, #1a1a1a 25%, transparent 25%),
                        linear-gradient(-45deg, #1a1a1a 25%, transparent 25%),
                        linear-gradient(45deg, transparent 75%, #1a1a1a 75%),
                        linear-gradient(-45deg, transparent 75%, #1a1a1a 75%);
                    background-size: 20px 20px;
                    background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
                    background-color: #0a0a0a;
                    cursor: grab;
                }}

                .viewer-content.panning {{
                    cursor: grabbing;
                }}

                .viewer-image {{
                    max-width: 90%;
                    max-height: 90%;
                    object-fit: contain;
                    transition: transform 0.2s ease;
                    user-select: none;
                }}

                .zoom-controls {{
                    position: absolute;
                    bottom: 1.5rem;
                    left: 50%;
                    transform: translateX(-50%);
                    display: flex;
                    gap: 0.5rem;
                    background: #171717;
                    border: 1px solid #262626;
                    border-radius: 0.5rem;
                    padding: 0.5rem;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
                    z-index: 10;
                }}

                .zoom-btn {{
                    background: #262626;
                    border: 1px solid #3f3f46;
                    color: #fafafa;
                    width: 36px;
                    height: 36px;
                    border-radius: 0.375rem;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                    transition: all 0.2s;
                    font-size: 18px;
                    font-weight: 600;
                }}

                .zoom-btn:hover {{
                    background: #3f3f46;
                    border-color: #a1a1aa;
                }}

                .zoom-btn:active {{
                    transform: scale(0.95);
                }}

                .zoom-level {{
                    position: absolute;
                    top: 1rem;
                    right: 1rem;
                    background: rgba(23, 23, 23, 0.9);
                    border: 1px solid #262626;
                    color: #fafafa;
                    padding: 0.5rem 1rem;
                    border-radius: 0.5rem;
                    font-size: 0.875rem;
                    font-weight: 500;
                    z-index: 10;
                }}
            </style>

            <div class="viewer-container">
                <div class="viewer-header">
                    <span>📷 Imagen Original</span>
                    <span style="font-size: 0.875rem; color: #a1a1aa;">Usa la rueda del mouse o los controles para hacer zoom</span>
                </div>
                <div class="viewer-content" id="viewer-content">
                    <img src="data:image/png;base64,{img_str}"
                         class="viewer-image"
                         id="viewer-image"
                         draggable="false">
                    <div class="zoom-level" id="zoom-level">100%</div>
                </div>
                <div class="zoom-controls">
                    <button class="zoom-btn" onclick="zoomOut()" title="Alejar">−</button>
                    <button class="zoom-btn" onclick="zoomReset()" title="Restablecer">⊙</button>
                    <button class="zoom-btn" onclick="zoomIn()" title="Acercar">+</button>
                    <button class="zoom-btn" onclick="togglePan()" id="pan-btn" title="Activar paneo">✋</button>
                </div>
            </div>

            <script>
                let zoom = 1;
                let panX = 0;
                let panY = 0;
                let isPanning = false;
                let startX = 0;
                let startY = 0;
                let panMode = false;

                const image = document.getElementById('viewer-image');
                const container = document.getElementById('viewer-content');
                const zoomLevelDisplay = document.getElementById('zoom-level');

                function updateTransform() {{
                    image.style.transform = `translate(${{panX}}px, ${{panY}}px) scale(${{zoom}})`;
                    zoomLevelDisplay.textContent = Math.round(zoom * 100) + '%';
                }}

                function zoomIn() {{
                    zoom = Math.min(zoom * 1.2, 10);
                    updateTransform();
                }}

                function zoomOut() {{
                    zoom = Math.max(zoom / 1.2, 0.1);
                    updateTransform();
                }}

                function zoomReset() {{
                    zoom = 1;
                    panX = 0;
                    panY = 0;
                    updateTransform();
                }}

                function togglePan() {{
                    panMode = !panMode;
                    const panBtn = document.getElementById('pan-btn');
                    if (panMode) {{
                        container.style.cursor = 'grab';
                        panBtn.style.background = '#3f3f46';
                        panBtn.style.borderColor = '#fafafa';
                    }} else {{
                        container.style.cursor = 'default';
                        panBtn.style.background = '#262626';
                        panBtn.style.borderColor = '#3f3f46';
                    }}
                }}

                // Zoom con rueda del mouse
                container.addEventListener('wheel', (e) => {{
                    e.preventDefault();
                    const delta = e.deltaY > 0 ? 0.9 : 1.1;
                    zoom = Math.min(Math.max(zoom * delta, 0.1), 10);
                    updateTransform();
                }});

                // Pan con arrastre
                container.addEventListener('mousedown', (e) => {{
                    if (panMode) {{
                        isPanning = true;
                        startX = e.clientX - panX;
                        startY = e.clientY - panY;
                        container.classList.add('panning');
                    }}
                }});

                container.addEventListener('mousemove', (e) => {{
                    if (isPanning && panMode) {{
                        panX = e.clientX - startX;
                        panY = e.clientY - startY;
                        updateTransform();
                    }}
                }});

                container.addEventListener('mouseup', () => {{
                    isPanning = false;
                    container.classList.remove('panning');
                }});

                container.addEventListener('mouseleave', () => {{
                    isPanning = false;
                    container.classList.remove('panning');
                }});
            </script>
            """

            components.html(viewer_html, height=700, scrolling=False)

        except Exception as e:
            st.error(f"Error al mostrar la imagen: {str(e)}")
            self._render_empty_view()

    def _render_svg_view(self, svg_content):
        """Renderiza la vista SVG con zoom y pan"""
        # Modificar SVG para líneas blancas
        svg_modified = svg_content.replace('fill="black"', 'fill="white"')
        svg_modified = svg_modified.replace('stroke="black"', 'stroke="white"')
        if 'stroke=' not in svg_modified and 'fill=' not in svg_modified:
            svg_modified = svg_modified.replace('<path ', '<path stroke="white" fill="none" stroke-width="2" ')

        viewer_html = f"""
        <style>
            .viewer-container {{
                width: 100%;
                height: 80vh;
                background: #000000;
                border: 1px solid #262626;
                border-radius: 0.5rem;
                position: relative;
                overflow: hidden;
                display: flex;
                flex-direction: column;
            }}

            .viewer-header {{
                background: #171717;
                border-bottom: 1px solid #262626;
                padding: 0.75rem 1.25rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                color: #fafafa;
                font-weight: 500;
                font-size: 0.95rem;
                z-index: 10;
            }}

            .viewer-content {{
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                position: relative;
                background: #000000;
                cursor: grab;
            }}

            .viewer-content.panning {{
                cursor: grabbing;
            }}

            .viewer-content svg {{
                max-width: 90%;
                max-height: 90%;
                transition: transform 0.2s ease;
            }}

            .zoom-controls {{
                position: absolute;
                bottom: 1.5rem;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 0.5rem;
                background: #171717;
                border: 1px solid #262626;
                border-radius: 0.5rem;
                padding: 0.5rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
                z-index: 10;
            }}

            .zoom-btn {{
                background: #262626;
                border: 1px solid #3f3f46;
                color: #fafafa;
                width: 36px;
                height: 36px;
                border-radius: 0.375rem;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.2s;
                font-size: 18px;
                font-weight: 600;
            }}

            .zoom-btn:hover {{
                background: #3f3f46;
                border-color: #a1a1aa;
            }}

            .zoom-btn:active {{
                transform: scale(0.95);
            }}

            .zoom-level {{
                position: absolute;
                top: 1rem;
                right: 1rem;
                background: rgba(23, 23, 23, 0.9);
                border: 1px solid #262626;
                color: #fafafa;
                padding: 0.5rem 1rem;
                border-radius: 0.5rem;
                font-size: 0.875rem;
                font-weight: 500;
                z-index: 10;
            }}
        </style>

        <div class="viewer-container">
            <div class="viewer-header">
                <span>📐 Vista SVG</span>
                <span style="font-size: 0.875rem; color: #a1a1aa;">Archivo vectorial escalable</span>
            </div>
            <div class="viewer-content" id="svg-viewer-content">
                <div id="svg-wrapper">
                    {svg_modified}
                </div>
                <div class="zoom-level" id="svg-zoom-level">100%</div>
            </div>
            <div class="zoom-controls">
                <button class="zoom-btn" onclick="svgZoomOut()" title="Alejar">−</button>
                <button class="zoom-btn" onclick="svgZoomReset()" title="Restablecer">⊙</button>
                <button class="zoom-btn" onclick="svgZoomIn()" title="Acercar">+</button>
                <button class="zoom-btn" onclick="svgTogglePan()" id="svg-pan-btn" title="Activar paneo">✋</button>
            </div>
        </div>

        <script>
            let svgZoom = 1;
            let svgPanX = 0;
            let svgPanY = 0;
            let svgIsPanning = false;
            let svgStartX = 0;
            let svgStartY = 0;
            let svgPanMode = false;

            const svgWrapper = document.getElementById('svg-wrapper');
            const svgContainer = document.getElementById('svg-viewer-content');
            const svgZoomLevelDisplay = document.getElementById('svg-zoom-level');

            function updateSvgTransform() {{
                svgWrapper.style.transform = `translate(${{svgPanX}}px, ${{svgPanY}}px) scale(${{svgZoom}})`;
                svgZoomLevelDisplay.textContent = Math.round(svgZoom * 100) + '%';
            }}

            function svgZoomIn() {{
                svgZoom = Math.min(svgZoom * 1.2, 10);
                updateSvgTransform();
            }}

            function svgZoomOut() {{
                svgZoom = Math.max(svgZoom / 1.2, 0.1);
                updateSvgTransform();
            }}

            function svgZoomReset() {{
                svgZoom = 1;
                svgPanX = 0;
                svgPanY = 0;
                updateSvgTransform();
            }}

            function svgTogglePan() {{
                svgPanMode = !svgPanMode;
                const panBtn = document.getElementById('svg-pan-btn');
                if (svgPanMode) {{
                    svgContainer.style.cursor = 'grab';
                    panBtn.style.background = '#3f3f46';
                    panBtn.style.borderColor = '#fafafa';
                }} else {{
                    svgContainer.style.cursor = 'default';
                    panBtn.style.background = '#262626';
                    panBtn.style.borderColor = '#3f3f46';
                }}
            }}

            svgContainer.addEventListener('wheel', (e) => {{
                e.preventDefault();
                const delta = e.deltaY > 0 ? 0.9 : 1.1;
                svgZoom = Math.min(Math.max(svgZoom * delta, 0.1), 10);
                updateSvgTransform();
            }});

            svgContainer.addEventListener('mousedown', (e) => {{
                if (svgPanMode) {{
                    svgIsPanning = true;
                    svgStartX = e.clientX - svgPanX;
                    svgStartY = e.clientY - svgPanY;
                    svgContainer.classList.add('panning');
                }}
            }});

            svgContainer.addEventListener('mousemove', (e) => {{
                if (svgIsPanning && svgPanMode) {{
                    svgPanX = e.clientX - svgStartX;
                    svgPanY = e.clientY - svgStartY;
                    updateSvgTransform();
                }}
            }});

            svgContainer.addEventListener('mouseup', () => {{
                svgIsPanning = false;
                svgContainer.classList.remove('panning');
            }});

            svgContainer.addEventListener('mouseleave', () => {{
                svgIsPanning = false;
                svgContainer.classList.remove('panning');
            }});
        </script>
        """

        components.html(viewer_html, height=700, scrolling=False)

    def _render_dxf_view(self, svg_content):
        """Renderiza la vista DXF (usando SVG como preview) con líneas verde neón"""
        # Modificar SVG para líneas verde neón
        svg_modified = svg_content.replace('fill="black"', 'fill="none" stroke="#00ff41" stroke-width="2"')
        svg_modified = svg_modified.replace('stroke="black"', 'stroke="#00ff41"')
        if 'stroke=' not in svg_modified:
            svg_modified = svg_modified.replace('<path ', '<path stroke="#00ff41" fill="none" stroke-width="2" ')

        viewer_html = f"""
        <style>
            .viewer-container {{
                width: 100%;
                height: 80vh;
                background: #000000;
                border: 1px solid #262626;
                border-radius: 0.5rem;
                position: relative;
                overflow: hidden;
                display: flex;
                flex-direction: column;
            }}

            .viewer-header {{
                background: #171717;
                border-bottom: 1px solid #262626;
                padding: 0.75rem 1.25rem;
                display: flex;
                justify-content: space-between;
                align-items: center;
                color: #fafafa;
                font-weight: 500;
                font-size: 0.95rem;
                z-index: 10;
            }}

            .viewer-content {{
                flex: 1;
                display: flex;
                align-items: center;
                justify-content: center;
                overflow: hidden;
                position: relative;
                background: #000000;
                cursor: grab;
            }}

            .viewer-content.panning {{
                cursor: grabbing;
            }}

            .viewer-content svg {{
                max-width: 90%;
                max-height: 90%;
                transition: transform 0.2s ease;
            }}

            .zoom-controls {{
                position: absolute;
                bottom: 1.5rem;
                left: 50%;
                transform: translateX(-50%);
                display: flex;
                gap: 0.5rem;
                background: #171717;
                border: 1px solid #262626;
                border-radius: 0.5rem;
                padding: 0.5rem;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
                z-index: 10;
            }}

            .zoom-btn {{
                background: #262626;
                border: 1px solid #3f3f46;
                color: #fafafa;
                width: 36px;
                height: 36px;
                border-radius: 0.375rem;
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.2s;
                font-size: 18px;
                font-weight: 600;
            }}

            .zoom-btn:hover {{
                background: #3f3f46;
                border-color: #a1a1aa;
            }}

            .zoom-btn:active {{
                transform: scale(0.95);
            }}

            .zoom-level {{
                position: absolute;
                top: 1rem;
                right: 1rem;
                background: rgba(23, 23, 23, 0.9);
                border: 1px solid #262626;
                color: #00ff41;
                padding: 0.5rem 1rem;
                border-radius: 0.5rem;
                font-size: 0.875rem;
                font-weight: 500;
                z-index: 10;
            }}
        </style>

        <div class="viewer-container">
            <div class="viewer-header">
                <span>🔧 Vista DXF (Preview)</span>
                <span style="font-size: 0.875rem; color: #a1a1aa;">Formato CAD para corte láser/CNC</span>
            </div>
            <div class="viewer-content" id="dxf-viewer-content">
                <div id="dxf-wrapper">
                    {svg_modified}
                </div>
                <div class="zoom-level" id="dxf-zoom-level">100%</div>
            </div>
            <div class="zoom-controls">
                <button class="zoom-btn" onclick="dxfZoomOut()" title="Alejar">−</button>
                <button class="zoom-btn" onclick="dxfZoomReset()" title="Restablecer">⊙</button>
                <button class="zoom-btn" onclick="dxfZoomIn()" title="Acercar">+</button>
                <button class="zoom-btn" onclick="dxfTogglePan()" id="dxf-pan-btn" title="Activar paneo">✋</button>
            </div>
        </div>

        <script>
            let dxfZoom = 1;
            let dxfPanX = 0;
            let dxfPanY = 0;
            let dxfIsPanning = false;
            let dxfStartX = 0;
            let dxfStartY = 0;
            let dxfPanMode = false;

            const dxfWrapper = document.getElementById('dxf-wrapper');
            const dxfContainer = document.getElementById('dxf-viewer-content');
            const dxfZoomLevelDisplay = document.getElementById('dxf-zoom-level');

            function updateDxfTransform() {{
                dxfWrapper.style.transform = `translate(${{dxfPanX}}px, ${{dxfPanY}}px) scale(${{dxfZoom}})`;
                dxfZoomLevelDisplay.textContent = Math.round(dxfZoom * 100) + '%';
            }}

            function dxfZoomIn() {{
                dxfZoom = Math.min(dxfZoom * 1.2, 10);
                updateDxfTransform();
            }}

            function dxfZoomOut() {{
                dxfZoom = Math.max(dxfZoom / 1.2, 0.1);
                updateDxfTransform();
            }}

            function dxfZoomReset() {{
                dxfZoom = 1;
                dxfPanX = 0;
                dxfPanY = 0;
                updateDxfTransform();
            }}

            function dxfTogglePan() {{
                dxfPanMode = !dxfPanMode;
                const panBtn = document.getElementById('dxf-pan-btn');
                if (dxfPanMode) {{
                    dxfContainer.style.cursor = 'grab';
                    panBtn.style.background = '#3f3f46';
                    panBtn.style.borderColor = '#fafafa';
                }} else {{
                    dxfContainer.style.cursor = 'default';
                    panBtn.style.background = '#262626';
                    panBtn.style.borderColor = '#3f3f46';
                }}
            }}

            dxfContainer.addEventListener('wheel', (e) => {{
                e.preventDefault();
                const delta = e.deltaY > 0 ? 0.9 : 1.1;
                dxfZoom = Math.min(Math.max(dxfZoom * delta, 0.1), 10);
                updateDxfTransform();
            }});

            dxfContainer.addEventListener('mousedown', (e) => {{
                if (dxfPanMode) {{
                    dxfIsPanning = true;
                    dxfStartX = e.clientX - dxfPanX;
                    dxfStartY = e.clientY - dxfPanY;
                    dxfContainer.classList.add('panning');
                }}
            }});

            dxfContainer.addEventListener('mousemove', (e) => {{
                if (dxfIsPanning && dxfPanMode) {{
                    dxfPanX = e.clientX - dxfStartX;
                    dxfPanY = e.clientY - dxfStartY;
                    updateDxfTransform();
                }}
            }});

            dxfContainer.addEventListener('mouseup', () => {{
                dxfIsPanning = false;
                dxfContainer.classList.remove('panning');
            }});

            dxfContainer.addEventListener('mouseleave', () => {{
                dxfIsPanning = false;
                dxfContainer.classList.remove('panning');
            }});
        </script>
        """

        components.html(viewer_html, height=700, scrolling=False)

    def _render_empty_view(self):
        """Renderiza una vista vacía cuando no hay contenido"""
        viewer_html = """
        <style>
            .viewer-container {
                width: 100%;
                height: 80vh;
                background: #000000;
                border: 1px solid #262626;
                border-radius: 0.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-direction: column;
                gap: 1rem;
            }

            .empty-icon {
                font-size: 5rem;
                opacity: 0.3;
            }

            .empty-text {
                color: #a1a1aa;
                font-size: 1.1rem;
                font-weight: 500;
            }

            .empty-subtext {
                color: #71717a;
                font-size: 0.875rem;
            }
        </style>

        <div class="viewer-container">
            <div class="empty-icon">🎨</div>
            <div class="empty-text">Sube una imagen para comenzar</div>
            <div class="empty-subtext">Convierte imágenes a formato vectorial (SVG y DXF)</div>
        </div>
        """

        components.html(viewer_html, height=700, scrolling=False)
