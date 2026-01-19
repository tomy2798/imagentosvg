# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Image to Vector Converter - A Streamlit-based web application that converts raster images (PNG, JPG) to clean vector formats (SVG, DXF). This is a clone of vectorizer.ai focused on producing high-quality DXF output with smooth lines and no stair-stepping artifacts for CAD/CNC applications.

## Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Vectorization**: VTracer (image to SVG conversion)
- **SVG Processing**: svgpathtools (parsing and manipulating SVG paths)
- **DXF Generation**: ezdxf (creating CAD-compatible DXF files)
- **Image Processing**: OpenCV (cv2) for preprocessing and edge detection

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit application
streamlit run main.py

# Run with auto-reload on file changes
streamlit run main.py --server.runOnSave true
```

## Core Architecture

### Processing Pipeline

The application follows a three-stage pipeline:

1. **Image → SVG (Vectorization)**
   - Input: Raster image (PNG/JPG)
   - Tool: VTracer
   - Output: SVG with vector paths
   - Key parameters: `colormode='binary'`, `mode='spline'` for smooth curves

2. **SVG → Path Extraction**
   - Input: SVG file
   - Tool: svgpathtools
   - Process: Parse SVG paths into geometric primitives (Line, CubicBezier, etc.)
   - Output: Python objects representing vector geometry

3. **Paths → DXF (CAD Export)**
   - Input: Parsed SVG paths
   - Tool: ezdxf
   - Process: Convert paths to DXF entities (lines, polylines, splines)
   - Output: Clean DXF file for laser cutting/CNC

### Optional Preprocessing Stage

For noisy or low-quality images, OpenCV preprocessing improves vectorization:
- Grayscale conversion
- Adaptive thresholding (OTSU)
- Morphological operations (noise reduction)
- Edge detection

## Critical Parameters for Quality Output

### VTracer Configuration

```python
vtracer.convert_image_to_svg_py(
    image_path='input.png',   # Input image path
    out_path='output.svg',    # Output SVG path
    colormode='binary',       # B&W mode for logos
    filter_speckle=4,         # Remove noise artifacts
    corner_threshold=60,      # Edge detection sensitivity (60-180)
    length_threshold=4.0,     # Minimum segment length
    mode='spline',            # Use splines for smooth curves (not 'polygon')
    splice_threshold=45,      # Merge nearby segments
    path_precision=8          # Coordinate decimal precision
)
```

**Key insight**: `mode='spline'` is essential for smooth DXF output without stair-stepping.

### Bezier to Polyline Conversion

When converting CubicBezier curves to DXF polylines:
- Use 20+ subdivisions for smooth approximation
- Higher subdivision count = smoother curves but larger file size
- Adjust based on curve complexity

## File Organization

The project follows a modular architecture with clear separation of concerns:

```
imagentosvg/
├── main.py                      # Application entry point
├── requirements.txt             # Python dependencies
├── README.md                    # User documentation
├── CLAUDE.md                    # Development guide
├── .gitignore                   # Git ignore rules
├── src/
│   ├── core/                    # Core processing logic
│   │   ├── preprocessor.py      # Image preprocessing (ImagePreprocessor class)
│   │   ├── vectorizer.py        # SVG vectorization (ImageVectorizer class)
│   │   ├── dxf_converter.py     # DXF conversion (DXFConverter class)
│   │   └── pipeline.py          # Orchestrates full workflow (ProcessingPipeline class)
│   ├── ui/                      # User interface components
│   │   ├── sidebar.py           # Configuration sidebar (Sidebar class)
│   │   └── main_view.py         # Main view and results (MainView class)
│   └── utils/                   # Utilities and configuration
│       └── config.py            # Constants and default configurations
├── venv/                        # Virtual environment (git-ignored)
└── temp/                        # Temporary files during processing (git-ignored)
```

### Module Responsibilities

- **main.py**: Entry point that initializes the Streamlit app and coordinates UI components
- **core/preprocessor.py**: Handles image cleaning (grayscale, thresholding, noise reduction)
- **core/vectorizer.py**: Wraps VTracer for image-to-SVG conversion
- **core/dxf_converter.py**: Converts SVG paths to DXF entities with curve subdivision
- **core/pipeline.py**: Orchestrates the complete workflow with temporary file management
- **ui/sidebar.py**: Renders configuration controls and returns config dictionary
- **ui/main_view.py**: Handles upload, results display, and download buttons
- **utils/config.py**: Centralized configuration and constants

## Key Implementation Notes

### DXF Entity Mapping

- **SVG Line** → DXF `add_line(start, end)`
- **SVG CubicBezier** → DXF `add_lwpolyline(points)` with curve subdivision
- **SVG Arc/QuadraticBezier** → Convert to polyline with point sampling

### Coordinate System

- SVG uses top-left origin, Y-axis down
- DXF uses bottom-left origin, Y-axis up
- May need Y-coordinate inversion: `y_dxf = max_y - y_svg`

### Error Handling

- Handle malformed SVG paths gracefully
- Validate image formats before processing
- Provide clear error messages for unsupported features

## Dependencies

Core libraries:
- `streamlit` - Web UI framework
- `vtracer` - Image vectorization engine
- `ezdxf` - DXF file generation
- `svgpathtools` - SVG path parsing
- `opencv-python` (cv2) - Image preprocessing
- `numpy` - Array operations for OpenCV

## Quality Metrics

The primary goal is DXF output quality for CAD/CNC applications:
- **No stair-stepping**: Smooth curves, not jagged approximations
- **Clean geometry**: Minimal redundant points
- **Proper scaling**: Maintain aspect ratio and dimensions
- **CAD compatibility**: Works in AutoCAD, Fusion 360, etc.
