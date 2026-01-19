"""
Script de prueba para diagnosticar el problema de coordenadas DXF
"""

from svgpathtools import svg2paths
import numpy as np
import re

# Buscar el SVG de River Plate
svg_path = r"C:\Users\tomy2\Downloads\vectorizado.svg"

def parse_translate(transform_str):
    if not transform_str:
        return 0, 0
    match = re.search(r'translate\s*\(\s*([+-]?\d+\.?\d*)\s*[,\s]\s*([+-]?\d+\.?\d*)\s*\)', transform_str)
    if match:
        return float(match.group(1)), float(match.group(2))
    return 0, 0

try:
    paths, attributes = svg2paths(svg_path)

    print(f"Número de paths encontrados: {len(paths)}")
    print("\n" + "="*50)

    # Mostrar transformaciones
    for i, attr in enumerate(attributes[:3]):
        transform = attr.get('transform', '')
        tx, ty = parse_translate(transform)
        print(f"Path {i}: transform='{transform}'")
        print(f"  Traducción: ({tx}, {ty})")

    print("\n" + "="*50)

    # Recolectar todos los puntos
    all_points = []

    for i, path in enumerate(paths[:3]):  # Solo primeros 3 paths para debug
        print(f"\nPath {i}: {len(path)} segmentos")

        for j, segment in enumerate(path[:2]):  # Solo primeros 2 segmentos
            print(f"  Segmento {j}: {type(segment).__name__}")
            print(f"    Start: ({segment.start.real:.2f}, {segment.start.imag:.2f})")
            print(f"    End: ({segment.end.real:.2f}, {segment.end.imag:.2f})")

            all_points.append(segment.start)
            all_points.append(segment.end)

    # Calcular límites
    if all_points:
        x_coords = [p.real for p in all_points]
        y_coords = [p.imag for p in all_points]

        print("\n" + "="*50)
        print("LÍMITES DEL SVG:")
        print(f"X: min={min(x_coords):.2f}, max={max(x_coords):.2f}")
        print(f"Y: min={min(y_coords):.2f}, max={max(y_coords):.2f}")
        print(f"Ancho: {max(x_coords) - min(x_coords):.2f}")
        print(f"Alto: {max(y_coords) - min(y_coords):.2f}")

        # Simular transformación actual
        svg_height = max(y_coords)
        y_min = min(y_coords)

        print("\n" + "="*50)
        print("VALORES CALCULADOS:")
        print(f"svg_height: {svg_height:.2f}")
        print(f"y_min: {y_min:.2f}")

        # Probar transformación de un punto
        test_point = all_points[0]
        y = test_point.imag
        y_inverted = svg_height - (y - y_min)

        print("\n" + "="*50)
        print("PRUEBA DE TRANSFORMACIÓN:")
        print(f"Punto original: ({test_point.real:.2f}, {test_point.imag:.2f})")
        print(f"Y transformado: {y_inverted:.2f}")
        print(f"Fórmula: {svg_height:.2f} - ({y:.2f} - {y_min:.2f}) = {y_inverted:.2f}")

except FileNotFoundError:
    print("No se encontró el archivo SVG. Verifica la ruta.")
except Exception as e:
    print(f"Error: {e}")
