"""
Script de prueba para la conversión SVG a DXF con transformaciones
"""

from src.core.dxf_converter_v2 import DXFConverterV2

# Rutas de archivos
svg_input = r"C:\Users\tomy2\Downloads\vectorizado.svg"
dxf_output = r"C:\Users\tomy2\Downloads\test_output.dxf"

# Crear convertidor
converter = DXFConverterV2(
    bezier_subdivisions=30,
    use_splines=True,
    tolerance=0.1
)

# Convertir
print("Iniciando conversión SVG a DXF...")
success, message = converter.convert(svg_input, dxf_output)

if success:
    print(f"OK - {message}")
    print(f"Archivo DXF guardado en: {dxf_output}")
else:
    print(f"ERROR: {message}")
