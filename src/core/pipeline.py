"""
Módulo de pipeline de procesamiento
Coordina el flujo completo: Imagen → SVG → DXF
"""

import os
import tempfile
from PIL import Image
import numpy as np

from .preprocessor import ImagePreprocessor
from .vectorizer import ImageVectorizer
from .dxf_converter_v2 import DXFConverterV2


class ProcessingPipeline:
    """Pipeline completo de conversión de imagen a vector"""

    def __init__(
        self,
        use_preprocessing=True,
        preprocessor_config=None,
        vectorizer_config=None,
        dxf_config=None
    ):
        """
        Inicializa el pipeline de procesamiento

        Args:
            use_preprocessing: Si se debe aplicar preprocesamiento
            preprocessor_config: Configuración del preprocesador (dict)
            vectorizer_config: Configuración del vectorizador (dict)
            dxf_config: Configuración del convertidor DXF (dict)
        """
        self.use_preprocessing = use_preprocessing

        # Inicializar módulos
        self.preprocessor = ImagePreprocessor(**(preprocessor_config or {}))
        self.vectorizer = ImageVectorizer(**(vectorizer_config or {}))
        self.dxf_converter = DXFConverterV2(**(dxf_config or {}))

    def process(self, uploaded_file, progress_callback=None):
        """
        Procesa una imagen a través del pipeline completo

        Args:
            uploaded_file: Archivo subido (file-like object)
            progress_callback: Función callback para reportar progreso (opcional)

        Returns:
            tuple: (results: dict, message: str)
        """
        results = {
            'preprocessing': None,
            'svg': None,
            'dxf': None,
            'svg_path': None,
            'dxf_path': None
        }

        # Crear directorio temporal
        with tempfile.TemporaryDirectory() as tmp_dir:
            try:
                # Reportar inicio
                if progress_callback:
                    progress_callback('loading', 10)

                # Cargar imagen
                image = Image.open(uploaded_file)
                image_array = np.array(image)

                # Reportar progreso: Preprocesamiento
                if progress_callback:
                    progress_callback('preprocessing', 20)

                # Paso 1: Preprocesamiento (opcional)
                input_path = self._preprocess_image(
                    image, image_array, tmp_dir, results
                )

                # Reportar progreso: Vectorización
                if progress_callback:
                    progress_callback('vectorizing', 40)

                # Paso 2: Imagen → SVG
                svg_path = os.path.join(tmp_dir, "output.svg")
                success, message = self.vectorizer.convert(input_path, svg_path)

                if not success:
                    return results, message

                # Leer SVG para retornar
                with open(svg_path, 'r', encoding='utf-8') as f:
                    results['svg'] = f.read()
                results['svg_path'] = svg_path

                # Reportar progreso: Conversión DXF
                if progress_callback:
                    progress_callback('converting', 70)

                # Paso 3: SVG → DXF
                dxf_path = os.path.join(tmp_dir, "output.dxf")
                success, message = self.dxf_converter.convert(svg_path, dxf_path)

                if not success:
                    return results, message

                # Leer DXF para retornar
                with open(dxf_path, 'rb') as f:
                    results['dxf'] = f.read()
                results['dxf_path'] = dxf_path

                # Reportar finalización
                if progress_callback:
                    progress_callback('completed', 100)

                return results, "✅ Procesamiento completado exitosamente"

            except Exception as e:
                return results, f"❌ Error en el pipeline: {str(e)}"

    def _preprocess_image(self, image, image_array, tmp_dir, results):
        """
        Preprocesa la imagen si está habilitado

        Args:
            image: Imagen PIL original
            image_array: Array numpy de la imagen
            tmp_dir: Directorio temporal
            results: Diccionario de resultados

        Returns:
            str: Ruta de la imagen procesada o original
        """
        if self.use_preprocessing:
            processed_image = self.preprocessor.process_pil_image(image)
            results['preprocessing'] = processed_image

            # Guardar imagen procesada
            input_path = os.path.join(tmp_dir, "input_processed.png")
            processed_image.save(input_path)
            return input_path
        else:
            # Guardar imagen original
            input_path = os.path.join(tmp_dir, "input.png")
            image.save(input_path)
            return input_path

    def update_config(
        self,
        use_preprocessing=None,
        preprocessor_config=None,
        vectorizer_config=None,
        dxf_config=None
    ):
        """Actualiza la configuración del pipeline"""
        if use_preprocessing is not None:
            self.use_preprocessing = use_preprocessing

        if preprocessor_config:
            self.preprocessor = ImagePreprocessor(**preprocessor_config)

        if vectorizer_config:
            self.vectorizer = ImageVectorizer(**vectorizer_config)

        if dxf_config:
            self.dxf_converter = DXFConverterV2(**dxf_config)
