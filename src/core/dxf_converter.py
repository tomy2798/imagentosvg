"""
Módulo de conversión SVG a DXF
Convierte paths SVG a entidades DXF para aplicaciones CAD/CNC
"""

import ezdxf
from svgpathtools import svg2paths, Line, CubicBezier, QuadraticBezier, Arc


class DXFConverter:
    """Convierte archivos SVG a formato DXF"""

    def __init__(self, bezier_subdivisions=20):
        """
        Inicializa el convertidor DXF

        Args:
            bezier_subdivisions: Número de subdivisiones para curvas Bezier (más = más suave)
        """
        self.bezier_subdivisions = bezier_subdivisions

    def convert(self, svg_input, dxf_output):
        """
        Convierte SVG a DXF

        Args:
            svg_input: Ruta del archivo SVG de entrada
            dxf_output: Ruta donde guardar el archivo DXF

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Leer los paths del SVG
            paths, attributes = svg2paths(svg_input)

            # Crear documento DXF
            doc = ezdxf.new('R2010')
            msp = doc.modelspace()

            # Convertir cada path SVG a entidades DXF
            for path in paths:
                self._convert_path(path, msp)

            # Guardar DXF
            doc.saveas(dxf_output)
            return True, "DXF generado exitosamente"

        except Exception as e:
            return False, f"Error al generar DXF: {str(e)}"

    def _convert_path(self, path, modelspace):
        """
        Convierte un path SVG individual a entidades DXF

        Args:
            path: Path SVG a convertir
            modelspace: Modelspace del documento DXF donde agregar las entidades
        """
        for segment in path:
            if isinstance(segment, Line):
                self._add_line(segment, modelspace)
            elif isinstance(segment, CubicBezier):
                self._add_cubic_bezier(segment, modelspace)
            elif isinstance(segment, QuadraticBezier):
                self._add_quadratic_bezier(segment, modelspace)
            elif isinstance(segment, Arc):
                self._add_arc(segment, modelspace)

    def _add_line(self, segment, modelspace):
        """Agrega una línea recta al DXF"""
        start = (segment.start.real, segment.start.imag)
        end = (segment.end.real, segment.end.imag)
        modelspace.add_line(start, end)

    def _add_cubic_bezier(self, segment, modelspace):
        """Convierte curva Bezier cúbica a polilínea"""
        points = self._subdivide_curve(segment)
        modelspace.add_lwpolyline(points)

    def _add_quadratic_bezier(self, segment, modelspace):
        """Convierte curva Bezier cuadrática a polilínea"""
        points = self._subdivide_curve(segment)
        modelspace.add_lwpolyline(points)

    def _add_arc(self, segment, modelspace):
        """Convierte arco a polilínea"""
        points = self._subdivide_curve(segment)
        modelspace.add_lwpolyline(points)

    def _subdivide_curve(self, segment):
        """
        Subdivide una curva en puntos para crear una polilínea suave

        Args:
            segment: Segmento de curva SVG

        Returns:
            Lista de tuplas (x, y) representando los puntos
        """
        points = []
        for i in range(self.bezier_subdivisions + 1):
            t = i / self.bezier_subdivisions
            point = segment.point(t)
            points.append((point.real, point.imag))
        return points

    def set_subdivisions(self, subdivisions):
        """Actualiza el número de subdivisiones para curvas"""
        self.bezier_subdivisions = max(10, min(50, subdivisions))
