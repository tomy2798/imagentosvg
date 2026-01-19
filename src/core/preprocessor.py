"""
Módulo de preprocesamiento de imágenes
Maneja la limpieza y preparación de imágenes antes de la vectorización
"""

import cv2
import numpy as np
from PIL import Image


class ImagePreprocessor:
    """Preprocesa imágenes para mejorar la calidad de vectorización"""

    def __init__(self, threshold_method="OTSU", threshold_value=127, noise_reduction=True, upscale_factor=1.0):
        """
        Inicializa el preprocesador de imágenes

        Args:
            threshold_method: Método de umbralización ("OTSU", "Adaptivo", "Manual")
            threshold_value: Valor de umbral para método manual (0-255)
            noise_reduction: Si se debe aplicar reducción de ruido
            upscale_factor: Factor de escalado para mejorar calidad (1.0 = sin cambio, 2.0 = doble tamaño)
        """
        self.threshold_method = threshold_method
        self.threshold_value = threshold_value
        self.noise_reduction = noise_reduction
        self.upscale_factor = upscale_factor

    def process(self, image_array):
        """
        Procesa la imagen aplicando preprocesamiento

        Args:
            image_array: Array numpy de la imagen

        Returns:
            Array numpy de la imagen procesada
        """
        # Convertir a escala de grises
        gray = self._convert_to_grayscale(image_array)

        # Aplicar umbralización
        binary = self._apply_threshold(gray)

        # Aplicar reducción de ruido si está activado
        if self.noise_reduction:
            binary = self._reduce_noise(binary)

        return binary

    def _convert_to_grayscale(self, image_array):
        """Convierte imagen a escala de grises"""
        if len(image_array.shape) == 3:
            return cv2.cvtColor(image_array, cv2.COLOR_RGB2GRAY)
        return image_array

    def _apply_threshold(self, gray_image):
        """Aplica umbralización según el método configurado"""
        if self.threshold_method == "OTSU":
            _, binary = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        elif self.threshold_method == "Adaptivo":
            binary = cv2.adaptiveThreshold(
                gray_image, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
        else:  # Manual
            _, binary = cv2.threshold(gray_image, self.threshold_value, 255, cv2.THRESH_BINARY)

        return binary

    def _reduce_noise(self, binary_image):
        """Aplica operaciones morfológicas para reducir ruido"""
        kernel = np.ones((3, 3), np.uint8)
        # Cierre: elimina pequeños agujeros
        binary = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)
        # Apertura: elimina pequeños puntos
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
        return binary

    def process_pil_image(self, pil_image):
        """
        Procesa una imagen PIL y devuelve imagen PIL procesada

        Args:
            pil_image: Imagen PIL

        Returns:
            Imagen PIL procesada
        """
        # Aplicar upscaling si está configurado
        if self.upscale_factor > 1.0:
            pil_image = self._upscale_image(pil_image)
        
        image_array = np.array(pil_image)
        processed_array = self.process(image_array)
        return Image.fromarray(processed_array)
    
    def _upscale_image(self, pil_image):
        """
        Aumenta la resolución de la imagen usando interpolación de alta calidad
        
        Args:
            pil_image: Imagen PIL original
            
        Returns:
            Imagen PIL con mayor resolución
        """
        original_size = pil_image.size
        new_size = (
            int(original_size[0] * self.upscale_factor),
            int(original_size[1] * self.upscale_factor)
        )
        # Usar LANCZOS para mejor calidad de interpolación
        return pil_image.resize(new_size, Image.Resampling.LANCZOS)
