"""
Módulo de estilos CSS personalizados
Define estilos visuales y animaciones para la aplicación
Tema oscuro inspirado en shadcn/ui
"""

def get_custom_css():
    """
    Retorna CSS personalizado para la aplicación

    Returns:
        str: CSS en formato HTML
    """
    return """
    <style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Variables de color - Paleta shadcn (Dark Mode) */
    :root {
        --background: #0a0a0a;
        --foreground: #fafafa;
        --card: #171717;
        --card-foreground: #fafafa;
        --popover: #171717;
        --popover-foreground: #fafafa;
        --primary: #fafafa;
        --primary-foreground: #0a0a0a;
        --secondary: #262626;
        --secondary-foreground: #fafafa;
        --muted: #262626;
        --muted-foreground: #a1a1aa;
        --accent: #262626;
        --accent-foreground: #fafafa;
        --destructive: #dc2626;
        --destructive-foreground: #fafafa;
        --border: #262626;
        --input: #262626;
        --ring: #fafafa;
        --success: #22c55e;
        --warning: #f59e0b;
        --radius: 0.5rem;
        --preview-bg: #e5e5e5;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.3);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.4);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }

    /* Reset y estilos base */
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: var(--background);
        color: var(--foreground);
    }

    /* Ocultar elementos de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    header {visibility: hidden;}

    /* Header personalizado */
    .custom-header {
        background: var(--card);
        padding: 2rem 2rem 2rem 2rem;
        border-bottom: 1px solid var(--border);
        margin: -1rem -1rem 2rem -1rem;
        color: var(--foreground);
        text-align: center;
    }

    .custom-header h1 {
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: var(--foreground);
    }

    .custom-header p {
        font-size: 0.95rem;
        color: var(--muted-foreground);
        font-weight: 400;
    }

    /* Cards personalizadas */
    .custom-card {
        background: var(--card);
        border-radius: var(--radius);
        padding: 1.25rem;
        border: 1px solid var(--border);
        margin-bottom: 1.5rem;
        transition: all 0.2s ease;
    }

    .custom-card:hover {
        border-color: var(--muted-foreground);
    }

    .custom-card h3 {
        color: var(--foreground);
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    /* Preview containers - Estilo vectorizer.io con patrón de tablero */
    .preview-container {
        background-image:
            linear-gradient(45deg, #f0f0f0 25%, transparent 25%),
            linear-gradient(-45deg, #f0f0f0 25%, transparent 25%),
            linear-gradient(45deg, transparent 75%, #f0f0f0 75%),
            linear-gradient(-45deg, transparent 75%, #f0f0f0 75%);
        background-size: 20px 20px;
        background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
        background-color: #ffffff;
        border-radius: var(--radius);
        padding: 0;
        margin: 1rem 0;
        border: 1px solid var(--border);
        min-height: 400px;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }

    .preview-image {
        max-width: 100%;
        height: auto;
        border-radius: 0;
    }

    /* Controles de zoom - Estilo vectorizer.io */
    .zoom-controls {
        position: absolute;
        bottom: 1rem;
        left: 50%;
        transform: translateX(-50%);
        display: flex;
        gap: 0.5rem;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 0.5rem;
        box-shadow: var(--shadow-md);
        z-index: 10;
    }

    .zoom-btn {
        background: var(--secondary);
        border: 1px solid var(--border);
        color: var(--foreground);
        width: 32px;
        height: 32px;
        border-radius: calc(var(--radius) - 2px);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s;
        font-size: 16px;
    }

    .zoom-btn:hover {
        background: var(--accent);
        border-color: var(--muted-foreground);
    }

    .zoom-btn:active {
        transform: scale(0.95);
    }

    /* Loading spinner personalizado */
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }

    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes progress {
        0% { left: -30%; }
        100% { left: 100%; }
    }

    .loading-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
        gap: 1rem;
    }

    .loading-spinner {
        width: 60px;
        height: 60px;
        border: 4px solid var(--border);
        border-top: 4px solid var(--foreground);
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }

    .loading-text {
        color: var(--muted-foreground);
        font-size: 1rem;
        font-weight: 500;
        animation: pulse 1.5s ease-in-out infinite;
    }

    .loading-progress {
        width: 100%;
        max-width: 400px;
        height: 4px;
        background: var(--border);
        border-radius: 2px;
        overflow: hidden;
        position: relative;
    }

    .loading-progress::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        height: 100%;
        width: 30%;
        background: var(--foreground);
        border-radius: 2px;
        animation: progress 1.5s ease-in-out infinite;
    }

    /* Botones personalizados */
    .stButton > button {
        background: var(--primary);
        color: var(--primary-foreground);
        border: none;
        border-radius: var(--radius);
        padding: 0.625rem 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: var(--secondary);
        color: var(--foreground);
    }

    .stButton > button:active {
        transform: scale(0.98);
    }

    /* Download buttons */
    .stDownloadButton > button {
        background: var(--success);
        color: white;
        border: none;
        border-radius: var(--radius);
        padding: 0.625rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
        width: 100%;
        margin-top: 0.5rem;
    }

    .stDownloadButton > button:hover {
        background: #16a34a;
    }

    /* Badge de estado */
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }

    .status-badge.success {
        background: rgba(34, 197, 94, 0.2);
        color: var(--success);
        border: 1px solid var(--success);
    }

    .status-badge.processing {
        background: rgba(245, 158, 11, 0.2);
        color: var(--warning);
        border: 1px solid var(--warning);
    }

    /* Sidebar mejorado */
    section[data-testid="stSidebar"] {
        background: var(--card);
        border-right: 1px solid var(--border);
    }

    section[data-testid="stSidebar"] .stMarkdown {
        color: var(--foreground);
    }

    /* Info boxes */
    .info-box {
        background: var(--card);
        border: 1px solid var(--border);
        border-left: 3px solid var(--muted-foreground);
        padding: 1rem;
        border-radius: var(--radius);
        margin: 1rem 0;
    }

    .info-box h4 {
        color: var(--foreground);
        margin: 0 0 0.5rem 0;
        font-size: 0.95rem;
        font-weight: 600;
    }

    .info-box p {
        margin: 0.25rem 0;
        color: var(--muted-foreground);
        font-size: 0.875rem;
    }

    /* Animation on load */
    .animate-in {
        animation: slideIn 0.3s ease-out;
    }

    /* SVG preview styling con patrón de tablero */
    .svg-preview {
        background-image:
            linear-gradient(45deg, #f0f0f0 25%, transparent 25%),
            linear-gradient(-45deg, #f0f0f0 25%, transparent 25%),
            linear-gradient(45deg, transparent 75%, #f0f0f0 75%),
            linear-gradient(-45deg, transparent 75%, #f0f0f0 75%);
        background-size: 20px 20px;
        background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
        background-color: #ffffff;
        padding: 2rem;
        border-radius: var(--radius);
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 400px;
        border: 1px solid var(--border);
        position: relative;
    }

    .svg-preview svg {
        max-width: 100%;
        max-height: 500px;
        height: auto;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--card);
        padding: 0.5rem;
        border-radius: var(--radius);
        border: 1px solid var(--border);
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border: none;
        color: var(--muted-foreground);
        padding: 0.5rem 1rem;
        border-radius: calc(var(--radius) - 2px);
        font-weight: 500;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background: var(--secondary);
        color: var(--foreground);
    }

    .stTabs [aria-selected="true"] {
        background: var(--secondary);
        color: var(--foreground);
    }

    /* File uploader styling */
    .stFileUploader {
        background: var(--muted);
        border: 2px dashed var(--border);
        border-radius: var(--radius);
        padding: 2rem;
    }

    .stFileUploader:hover {
        border-color: var(--muted-foreground);
    }

    /* Slider styling */
    .stSlider {
        padding: 1rem 0;
    }

    /* Selectbox styling */
    .stSelectbox {
        color: var(--foreground);
    }

    /* Checkbox styling */
    .stCheckbox {
        color: var(--foreground);
    }

    /* Expander styling */
    .streamlit-expanderHeader {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        color: var(--foreground);
        font-weight: 500;
    }

    .streamlit-expanderHeader:hover {
        border-color: var(--muted-foreground);
    }

    /* Compact header */
    .compact-header {
        background: var(--card);
        padding: 1rem 2rem;
        border-bottom: 1px solid var(--border);
        margin: -1rem -1rem 1rem -1rem;
        text-align: center;
    }

    .header-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--foreground);
    }

    /* Preview placeholder */
    .preview-placeholder {
        min-height: 500px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        margin: 2rem 0;
    }

    .placeholder-content {
        text-align: center;
        padding: 3rem;
    }

    /* Dark preview containers */
    .preview-dark-container {
        background: #000000;
        border: 1px solid var(--border);
        border-radius: var(--radius);
        overflow: hidden;
        min-height: 600px;
        position: relative;
        display: flex;
        flex-direction: column;
    }

    .preview-header {
        background: var(--card);
        border-bottom: 1px solid var(--border);
        padding: 0.75rem 1.25rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: var(--foreground);
        font-weight: 500;
        font-size: 0.95rem;
    }

    .preview-content {
        flex: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        overflow: hidden;
        position: relative;
    }

    .preview-dxf {
        background: #000000;
    }

    .preview-content svg {
        max-width: 100%;
        max-height: 100%;
        height: auto;
    }

    .download-btn {
        background: var(--success);
        color: white;
        border: none;
        border-radius: calc(var(--radius) - 2px);
        padding: 0.4rem 1rem;
        font-size: 0.875rem;
        font-weight: 500;
        cursor: pointer;
        transition: all 0.2s;
    }

    .download-btn:hover {
        background: #16a34a;
        transform: translateY(-1px);
    }

    .download-btn:active {
        transform: translateY(0);
    }

    .preview-empty {
        min-height: 400px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        color: var(--muted-foreground);
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .custom-header h1 {
            font-size: 1.5rem;
        }

        .zoom-controls {
            bottom: 0.5rem;
        }

        .preview-dark-container {
            min-height: 400px;
        }
    }

    /* Horizontal Thumbnails Strip */
    .thumbnails-container {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }

    .thumbnail-card {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 0.75rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 0.5rem;
    }

    .thumbnail-card:hover {
        border-color: var(--muted-foreground);
        transform: translateY(-2px);
    }

    .thumbnail-card.selected {
        border-color: var(--foreground);
        background: var(--secondary);
        box-shadow: 0 0 0 1px var(--foreground);
    }

    .thumbnail-preview {
        width: 100%;
        height: 120px;
        background: #ffffff;
        border-radius: calc(var(--radius) - 4px);
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        background-image:
            linear-gradient(45deg, #f0f0f0 25%, transparent 25%),
            linear-gradient(-45deg, #f0f0f0 25%, transparent 25%),
            linear-gradient(45deg, transparent 75%, #f0f0f0 75%),
            linear-gradient(-45deg, transparent 75%, #f0f0f0 75%);
        background-size: 10px 10px;
    }

    .thumbnail-preview.dark {
        background: #000000;
        background-image: none;
    }

    .thumbnail-preview img, .thumbnail-preview svg {
        max-width: 100%;
        max-height: 100%;
        object-fit: contain;
    }

    .thumbnail-title {
        font-size: 0.875rem;
        font-weight: 500;
        color: var(--foreground);
    }

    /* Main Viewer Area */
    .main-viewer {
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: var(--radius);
        padding: 1.5rem;
        min-height: 600px;
        display: flex;
        flex-direction: column;
    }

    .viewer-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border);
    }

    .viewer-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--foreground);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    </style>
    """

def get_loading_animation(text="Procesando..."):
    """
    Retorna HTML para animación de carga

    Args:
        text: Texto a mostrar durante la carga

    Returns:
        str: HTML con animación de carga
    """
    return f"""
    <div class="loading-container animate-in">
        <div class="loading-spinner"></div>
        <div class="loading-text">{text}</div>
        <div class="loading-progress"></div>
    </div>
    """

def get_status_badge(status="success", text="Completado"):
    """
    Retorna HTML para badge de estado

    Args:
        status: Tipo de estado (success, processing, error)
        text: Texto del badge

    Returns:
        str: HTML del badge
    """
    return f'<span class="status-badge {status}">{text}</span>'

def get_info_box(title, content):
    """
    Retorna HTML para caja de información

    Args:
        title: Título de la caja
        content: Contenido de la caja

    Returns:
        str: HTML de la caja de información
    """
    return f"""
    <div class="info-box animate-in">
        <h4>{title}</h4>
        <p>{content}</p>
    </div>
    """

def get_zoom_controls():
    """
    Retorna HTML para controles de zoom estilo vectorizer.io

    Returns:
        str: HTML de los controles de zoom
    """
    return """
    <div class="zoom-controls">
        <button class="zoom-btn" onclick="zoomOut()">−</button>
        <button class="zoom-btn" onclick="zoomReset()">⊙</button>
        <button class="zoom-btn" onclick="zoomIn()">+</button>
        <button class="zoom-btn" onclick="toggleFullscreen()">⛶</button>
    </div>
    <script>
        let currentZoom = 1;
        function zoomIn() {
            currentZoom = Math.min(currentZoom + 0.2, 3);
            updateZoom();
        }
        function zoomOut() {
            currentZoom = Math.max(currentZoom - 0.2, 0.5);
            updateZoom();
        }
        function zoomReset() {
            currentZoom = 1;
            updateZoom();
        }
        function updateZoom() {
            const svg = document.querySelector('.svg-preview svg, .preview-container svg');
            if (svg) {
                svg.style.transform = 'scale(' + currentZoom + ')';
                svg.style.transition = 'transform 0.2s ease';
            }
        }
        function toggleFullscreen() {
            const preview = document.querySelector('.svg-preview, .preview-container');
            if (preview) {
                if (!document.fullscreenElement) {
                    preview.requestFullscreen();
                } else {
                    document.exitFullscreen();
                }
            }
        }
    </script>
    """
