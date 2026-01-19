"""
Módulo de vectorización de imágenes
Convierte imágenes raster a formato SVG vectorizado
"""

import vtracer


class ImageVectorizer:
    """Convierte imágenes a formato SVG usando VTracer"""

    def __init__(
        self,
        color_mode="binary",
        filter_speckle=4,
        corner_threshold=60,
        length_threshold=4.0,
        mode="spline",
        splice_threshold=45,
        path_precision=8,
        color_precision=6,
        layer_difference=16,
        max_iterations=10,
        hierarchical="stacked"
    ):
        """
        Inicializa el vectorizador

        Args:
            color_mode: Modo de color ("binary" o "color")
            filter_speckle: Nivel de filtrado de manchas (0-10)
            corner_threshold: Umbral de detección de esquinas (0-180)
            length_threshold: Longitud máxima de segmentos (3.5-10) - valores más bajos = más detalle
            mode: Modo de curvas ("spline" para curvas suaves, "polygon" para segmentos rectos)
            splice_threshold: Ángulo mínimo para unir splines (0-180)
            path_precision: Precisión de decimales en coordenadas SVG (0-10)
            color_precision: Bits significativos por canal RGB (1-8, solo para modo color)
            layer_difference: Diferencia de color entre capas de gradiente (1-255, solo para modo color)
            max_iterations: Iteraciones máximas de algoritmos internos (1-20)
            hierarchical: Estrategia de clustering ("stacked" o "cutout", solo para modo color)
        """
        self.color_mode = color_mode
        self.filter_speckle = filter_speckle
        self.corner_threshold = corner_threshold
        self.length_threshold = length_threshold
        self.mode = mode
        self.splice_threshold = splice_threshold
        self.path_precision = path_precision
        self.color_precision = color_precision
        self.layer_difference = layer_difference
        self.max_iterations = max_iterations
        self.hierarchical = hierarchical

    def convert(self, input_path, output_path):
        """
        Convierte imagen a SVG

        Args:
            input_path: Ruta de la imagen de entrada
            output_path: Ruta donde guardar el SVG

        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            vtracer.convert_image_to_svg_py(
                image_path=input_path,
                out_path=output_path,
                colormode=self.color_mode,
                hierarchical=self.hierarchical,
                mode=self.mode,
                filter_speckle=self.filter_speckle,
                color_precision=self.color_precision,
                layer_difference=self.layer_difference,
                corner_threshold=self.corner_threshold,
                length_threshold=self.length_threshold,
                max_iterations=self.max_iterations,
                splice_threshold=self.splice_threshold,
                path_precision=self.path_precision
            )
            return True, "SVG generado exitosamente"
        except Exception as e:
            return False, f"Error al generar SVG: {str(e)}"

    def get_config(self):
        """Retorna la configuración actual del vectorizador"""
        return {
            "color_mode": self.color_mode,
            "filter_speckle": self.filter_speckle,
            "corner_threshold": self.corner_threshold,
            "length_threshold": self.length_threshold,
            "mode": self.mode,
            "splice_threshold": self.splice_threshold,
            "path_precision": self.path_precision,
            "color_precision": self.color_precision,
            "layer_difference": self.layer_difference,
            "max_iterations": self.max_iterations,
            "hierarchical": self.hierarchical
        }
