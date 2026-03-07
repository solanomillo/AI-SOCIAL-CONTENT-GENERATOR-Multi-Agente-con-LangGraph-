"""
Cliente profesional para Gemini API.
Maneja la comunicación con el modelo con reintentos y logging.
"""

import os
import json
import logging
import re
import time
from typing import Dict, Any, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors

from infrastructure.token_manager import TokenManager

load_dotenv()
logger = logging.getLogger(__name__)


class ClienteGemini:
    """
    Cliente robusto para Gemini API.
    """

    def __init__(
        self,
        model_name: Optional[str] = None,
        temperature: float = 0.7,
        max_output_tokens: int = 2048
    ):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY no configurada")

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name or os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

        logger.info(f"✅ Cliente Gemini inicializado: {self.model_name}")

    def _limpiar_json(self, texto: str) -> str:
        """Limpia la respuesta para extraer JSON válido."""
        if not texto:
            return "{}"

        # Eliminar markdown
        texto = re.sub(r"```(?:json)?", "", texto)
        texto = re.sub(r"```", "", texto)
        texto = texto.strip()

        # Balancear llaves si es necesario
        open_braces = texto.count("{")
        close_braces = texto.count("}")
        if open_braces > close_braces:
            texto += "}" * (open_braces - close_braces)

        return texto

    def generar_texto(self, prompt: str, max_reintentos: int = 2) -> str:
        """
        Genera texto con reintentos para errores transitorios.
        """
        prompt = TokenManager.recortar_texto(prompt, limite=500)

        for intento in range(max_reintentos):
            try:
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt,
                    config={
                        "temperature": self.temperature,
                        "max_output_tokens": self.max_output_tokens,
                    },
                )

                if not response or not response.text:
                    raise ValueError("Respuesta vacía del modelo")

                return response.text.strip()

            except genai_errors.ServerError as e:
                if "503" in str(e) and intento < max_reintentos - 1:
                    time.sleep((intento + 1) * 2)
                    continue
                raise

            except Exception as e:
                if intento < max_reintentos - 1:
                    time.sleep(1)
                    continue
                logger.error(f"Error generando texto: {e}")
                raise

        raise RuntimeError("No se pudo generar texto después de reintentos")

    def generar_json(self, prompt: str, max_reintentos: int = 2) -> Dict[str, Any]:
        """
        Genera y parsea JSON con manejo mejorado.
        """
        for intento in range(max_reintentos):
            try:
                texto = self.generar_texto(prompt, max_reintentos=1)
                
                # Limpiar el texto - eliminar todo lo que no sea JSON
                texto = texto.strip()
                
                # Buscar el primer { y el último }
                inicio = texto.find('{')
                fin = texto.rfind('}')
                
                if inicio != -1 and fin != -1 and fin > inicio:
                    texto_json = texto[inicio:fin+1]
                    data = json.loads(texto_json)
                    logger.info(f"✅ JSON parseado")
                    return data
                else:
                    logger.warning(f"No se encontró JSON válido en: {texto[:100]}")
                    
            except Exception as e:
                logger.warning(f"Intento {intento + 1} falló: {e}")
                
        return {}


def verificar_cuota() -> bool:
    """
    Verifica si hay cuota disponible.
    Usa el mismo modelo y configuración que los agentes.
    """
    try:
        # Usar EXACTAMENTE el mismo modelo que los agentes
        cliente = ClienteGemini(
            model_name="gemini-2.5-flash",  # Mismo modelo
            temperature=0.1, 
            max_output_tokens=5
        )
        
        # Hacer una llamada real (no solo inicializar)
        cliente.generar_texto("OK", max_reintentos=1)
        logger.info("✅ Verificación de cuota: disponible")
        return True
        
    except Exception as e:
        error_str = str(e).lower()
        logger.error(f"Error en verificación: {error_str[:200]}")
        
        # Detectar específicamente error 429 (cuota agotada)
        if "429" in error_str or "quota" in error_str or "resource_exhausted" in error_str:
            logger.warning("⚠️ Cuota agotada detectada en verificación")
            return False
            
        # Si es otro error (503, timeout, etc.), asumimos que hay cuota
        logger.warning(f"⚠️ Error inesperado en verificación, asumiendo cuota disponible: {error_str[:100]}")
        return True