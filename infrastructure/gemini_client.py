"""
Cliente base profesional para interactuar con Google Gemini.
Versión robusta y segura para arquitectura multi-agente.
"""

import os
from typing import Optional
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()


class ClienteGemini:
    """
    Cliente wrapper profesional para Gemini.
    Maneja errores y respuestas vacías correctamente.
    """

    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("No se encontró la variable de entorno GEMINI_API_KEY.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generar(self, prompt: str) -> str:
        """
        Genera contenido a partir de un prompt.
        Siempre devuelve string válido o lanza excepción controlada.
        """
        try:
            response = self.model.generate_content(prompt)

            if not response:
                raise ValueError("La respuesta del modelo está vacía.")

            # Forma segura de extraer texto
            if hasattr(response, "text") and response.text:
                return response.text.strip()

            # Fallback por si la estructura cambia
            if hasattr(response, "candidates") and response.candidates:
                parts = response.candidates[0].content.parts
                if parts:
                    return parts[0].text.strip()

            raise ValueError("No se pudo extraer texto de la respuesta del modelo.")

        except Exception as e:
            raise RuntimeError(f"Error al generar contenido con Gemini: {str(e)}")