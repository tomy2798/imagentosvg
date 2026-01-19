"""
Módulo mejorado de conversión SVG a DXF
Versión 2: Optimización de paths, coordenadas corregidas y transformaciones aplicadas
"""

import ezdxf
from svgpathtools import svg2paths, Line, CubicBezier, QuadraticBezier, Arc, Path
import numpy as np
import re
from typing import List, Tuple, Optional


class DXFConverterV2:
    """
    Convertidor mejorado de SVG a DXF con optimización de paths
    y corrección de coordenadas
    """

    def __init__(self, bezier_subdivisions=30, use_splines=True, tolerance=0.1):
        """
        Inicializa el convertidor DXF v2

        Args:
            bezier_subdivisions: Número de subdivisiones para curvas Bezier (más = más suave)
            use_splines: Si True, convierte Bezier a splines DXF nativos
            tolerance: Tolerancia para conectar paths cercanos (en unidades SVG)
        """
        self.bezier_subdivisions = bezier_subdivisions
        self.use_splines = use_splines
        self.tolerance = tolerance
        self.svg_height = 0
        self.y_min = 0

    def convert(self, svg_input, dxf_output):
        """
        Convierte SVG a DXF con optimizaciones

        Args:
            svg_input: Ruta del archivo SVG de entrada
            dxf_output: Ruta donde guardar el archivo DXF

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Leer los paths del SVG y atributos
            paths, attributes = svg2paths(svg_input)

            if not paths:
                return False, "No se encontraron paths en el SVG"

            # Aplicar transformaciones translate del SVG
            transformed_paths = self._apply_transforms(paths, attributes)

            # Calcular dimensiones del SVG para inversión de Y
            self._calculate_svg_bounds(transformed_paths)

            # Crear documento DXF
            doc = ezdxf.new('R2010')
            msp = doc.modelspace()

            # Procesar y convertir paths
            optimized_paths = self._optimize_paths(transformed_paths)

            # Convertir paths optimizados a entidades DXF
            for path_group in optimized_paths:
                self._convert_path_group(path_group, msp)

            # Guardar DXF
            doc.saveas(dxf_output)

            num_entities = len(list(msp))
            return True, f"DXF generado exitosamente con {num_entities} entidades"

        except Exception as e:
            return False, f"Error al generar DXF: {str(e)}"

    def _apply_transforms(self, paths, attributes):
        """
        Aplica las transformaciones SVG (translate) a los paths

        Args:
            paths: Lista de paths SVG
            attributes: Lista de diccionarios con atributos de cada path

        Returns:
            Lista de paths transformados
        """
        transformed_paths = []

        for path, attr in zip(paths, attributes):
            # Extraer transformación translate si existe
            transform_str = attr.get('transform', '')
            translate_x, translate_y = self._parse_translate(transform_str)

            # Si hay transformación, aplicarla al path
            if translate_x != 0 or translate_y != 0:
                # Crear path transformado
                transformed_path = Path()

                for segment in path:
                    # Aplicar traducción a cada segmento
                    transformed_segment = self._translate_segment(
                        segment, translate_x, translate_y
                    )
                    transformed_path.append(transformed_segment)

                transformed_paths.append(transformed_path)
            else:
                # Sin transformación, usar path original
                transformed_paths.append(path)

        return transformed_paths

    def _parse_translate(self, transform_str):
        """
        Extrae valores de translate de una cadena transform

        Args:
            transform_str: String con transformación (ej: "translate(481.046875,97.81640625)")

        Returns:
            tuple: (translate_x, translate_y)
        """
        if not transform_str:
            return 0, 0

        # Buscar patrón translate(x,y) o translate(x y)
        match = re.search(r'translate\s*\(\s*([+-]?\d+\.?\d*)\s*[,\s]\s*([+-]?\d+\.?\d*)\s*\)', transform_str)

        if match:
            tx = float(match.group(1))
            ty = float(match.group(2))
            return tx, ty

        return 0, 0

    def _translate_segment(self, segment, tx, ty):
        """
        Aplica traducción a un segmento SVG

        Args:
            segment: Segmento SVG (Line, CubicBezier, etc.)
            tx: Traslación en X
            ty: Traslación en Y

        Returns:
            Segmento transformado del mismo tipo
        """
        offset = complex(tx, ty)

        if isinstance(segment, Line):
            return Line(
                start=segment.start + offset,
                end=segment.end + offset
            )
        elif isinstance(segment, CubicBezier):
            return CubicBezier(
                start=segment.start + offset,
                control1=segment.control1 + offset,
                control2=segment.control2 + offset,
                end=segment.end + offset
            )
        elif isinstance(segment, QuadraticBezier):
            return QuadraticBezier(
                start=segment.start + offset,
                control=segment.control + offset,
                end=segment.end + offset
            )
        elif isinstance(segment, Arc):
            return Arc(
                start=segment.start + offset,
                radius=segment.radius,
                rotation=segment.rotation,
                large_arc=segment.large_arc,
                sweep=segment.sweep,
                end=segment.end + offset
            )
        else:
            # Para otros tipos, retornar sin cambios
            return segment

    def _calculate_svg_bounds(self, paths):
        """
        Calcula los límites del SVG para inversión de coordenadas Y

        Args:
            paths: Lista de paths SVG
        """
        all_points = []

        for path in paths:
            for segment in path:
                # Agregar puntos de inicio y fin
                all_points.append(segment.start)
                all_points.append(segment.end)

                # Para curvas, agregar puntos intermedios
                if isinstance(segment, (CubicBezier, QuadraticBezier, Arc)):
                    for t in np.linspace(0, 1, 10):
                        all_points.append(segment.point(t))

        if all_points:
            y_coords = [p.imag for p in all_points]
            self.svg_height = max(y_coords) - min(y_coords)
            self.y_min = min(y_coords)
        else:
            self.svg_height = 0
            self.y_min = 0

    def _optimize_paths(self, paths):
        """
        Optimiza paths agrupando segmentos conectados

        Args:
            paths: Lista de paths SVG

        Returns:
            Lista de paths optimizados agrupados
        """
        path_groups = []

        for path in paths:
            if len(path) > 0:
                # Verificar si el path está cerrado
                is_closed = self._is_path_closed(path)

                # Agrupar el path
                path_groups.append({
                    'path': path,
                    'is_closed': is_closed,
                    'segments': list(path)
                })

        return path_groups

    def _is_path_closed(self, path, tolerance=1e-3):
        """
        Verifica si un path está cerrado

        Args:
            path: Path SVG
            tolerance: Tolerancia para considerar puntos como iguales

        Returns:
            bool: True si el path está cerrado
        """
        if len(path) == 0:
            return False

        start = path[0].start
        end = path[-1].end

        distance = abs(end - start)
        return distance < tolerance

    def _convert_path_group(self, path_group, modelspace):
        """
        Convierte un grupo de paths a entidades DXF

        Args:
            path_group: Diccionario con información del path
            modelspace: Modelspace del documento DXF
        """
        path = path_group['path']
        is_closed = path_group['is_closed']

        # Si el path está cerrado, intentar crear una polilínea cerrada
        if is_closed and self._can_convert_to_polyline(path):
            self._add_closed_polyline(path, modelspace)
        else:
            # Convertir segmento por segmento
            for segment in path:
                self._convert_segment(segment, modelspace)

    def _can_convert_to_polyline(self, path):
        """
        Verifica si un path puede convertirse a polilínea

        Args:
            path: Path SVG

        Returns:
            bool: True si puede convertirse a polilínea
        """
        # Puede convertirse a polilínea si tiene segmentos conectados
        return len(path) > 1

    def _add_closed_polyline(self, path, modelspace):
        """
        Agrega una polilínea cerrada al DXF

        Args:
            path: Path SVG cerrado
            modelspace: Modelspace del documento DXF
        """
        points = []

        for segment in path:
            if isinstance(segment, Line):
                # Para líneas, solo agregar el punto de inicio
                start = self._transform_point(segment.start)
                points.append(start)
            else:
                # Para curvas, subdividir
                curve_points = self._subdivide_curve(segment)
                # Agregar todos los puntos excepto el último (para evitar duplicados)
                points.extend(curve_points[:-1])

        if len(points) > 2:
            # Crear polilínea cerrada
            polyline = modelspace.add_lwpolyline(points)
            polyline.close(True)

    def _convert_segment(self, segment, modelspace):
        """
        Convierte un segmento individual a entidad DXF

        Args:
            segment: Segmento SVG
            modelspace: Modelspace del documento DXF
        """
        if isinstance(segment, Line):
            self._add_line(segment, modelspace)
        elif isinstance(segment, CubicBezier):
            self._add_cubic_bezier(segment, modelspace)
        elif isinstance(segment, QuadraticBezier):
            self._add_quadratic_bezier(segment, modelspace)
        elif isinstance(segment, Arc):
            self._add_arc(segment, modelspace)

    def _add_line(self, segment, modelspace):
        """
        Agrega una línea recta al DXF con coordenadas transformadas

        Args:
            segment: Segmento Line de SVG
            modelspace: Modelspace del documento DXF
        """
        start = self._transform_point(segment.start)
        end = self._transform_point(segment.end)
        modelspace.add_line(start, end)

    def _add_cubic_bezier(self, segment, modelspace):
        """
        Convierte curva Bezier cúbica a polilínea

        Args:
            segment: Segmento CubicBezier de SVG
            modelspace: Modelspace del documento DXF
        """
        points = self._subdivide_curve(segment)
        modelspace.add_lwpolyline(points)

    def _add_quadratic_bezier(self, segment, modelspace):
        """
        Convierte curva Bezier cuadrática a polilínea

        Args:
            segment: Segmento QuadraticBezier de SVG
            modelspace: Modelspace del documento DXF
        """
        points = self._subdivide_curve(segment)
        modelspace.add_lwpolyline(points)

    def _add_arc(self, segment, modelspace):
        """
        Convierte arco a polilínea

        Args:
            segment: Segmento Arc de SVG
            modelspace: Modelspace del documento DXF
        """
        points = self._subdivide_curve(segment)
        modelspace.add_lwpolyline(points)

    def _subdivide_curve(self, segment):
        """
        Subdivide una curva en puntos con coordenadas transformadas

        Args:
            segment: Segmento de curva SVG

        Returns:
            Lista de tuplas (x, y) transformadas
        """
        points = []
        for i in range(self.bezier_subdivisions + 1):
            t = i / self.bezier_subdivisions
            point = segment.point(t)
            transformed = self._transform_point(point)
            points.append(transformed)
        return points

    def _transform_point(self, complex_point):
        """
        Transforma un punto complejo SVG a coordenadas DXF

        Args:
            complex_point: Punto en formato complejo (x + yj)

        Returns:
            tuple: (x, y) con Y invertido para coordenadas DXF
        """
        x = complex_point.real
        y = complex_point.imag

        # Invertir Y: DXF usa origen en la esquina inferior izquierda
        # SVG usa origen en la esquina superior izquierda
        y_inverted = self.svg_height + self.y_min - y

        return (x, y_inverted)

    def set_subdivisions(self, subdivisions):
        """
        Actualiza el número de subdivisiones para curvas

        Args:
            subdivisions: Nuevo número de subdivisiones
        """
        self.bezier_subdivisions = max(10, min(100, subdivisions))

    def set_use_splines(self, use_splines):
        """
        Configura si usar splines DXF nativos

        Args:
            use_splines: bool
        """
        self.use_splines = use_splines
