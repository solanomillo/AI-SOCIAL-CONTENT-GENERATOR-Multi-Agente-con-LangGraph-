"""
Cliente profesional para Tavily Search API.
Maneja la comunicación con Tavily de manera limpia y eficiente.
"""

import os
import logging
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv
from tavily import TavilyClient

from infrastructure.token_manager import TokenManager

load_dotenv()
logger = logging.getLogger(__name__)


class TavilyClientWrapper:
    """
    Cliente robusto para Tavily API.
    """

    def __init__(self):
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            error_msg = "TAVILY_API_KEY no configurada"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            self.client = TavilyClient(api_key=api_key)
            logger.info("✅ Cliente Tavily inicializado")
        except Exception as e:
            logger.error(f"Error inicializando Tavily: {e}")
            raise

    def buscar(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """
        Realiza búsqueda en Tavily.
        
        Args:
            query: Término de búsqueda
            max_results: Máximo de resultados
            
        Returns:
            Lista de resultados (vacía si hay error)
        """
        try:
            query = TokenManager.recortar_texto(query, limite=200)
            logger.info(f"🔍 Buscando: {query[:100]}...")

            response = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="advanced"
            )

            resultados = response.get("results", [])
            
            # Filtrar resultados sin contenido
            resultados_validos = [
                r for r in resultados 
                if r.get("content") and r.get("title")
            ]

            logger.info(f"✅ {len(resultados_validos)} resultados válidos")
            return resultados_validos

        except Exception as e:
            logger.error(f"Error en búsqueda Tavily: {e}")
            return []  # Retorna vacío, no rompe el flujo

    def extraer_contenido(self, resultados: List[Dict[str, Any]]) -> str:
        """
        Convierte resultados en texto plano para el LLM.
        
        Args:
            resultados: Lista de resultados de Tavily
            
        Returns:
            Texto formateado o string vacío
        """
        if not resultados:
            return ""

        try:
            textos = []
            LIMITE_TOTAL = 2000

            for i, r in enumerate(resultados[:3], 1):  # Límite a 3 resultados
                titulo = r.get("title", "Sin título")
                contenido = r.get("content", "")
                url = r.get("url", "")

                # Limitar cada resultado
                contenido = TokenManager.recortar_texto(contenido, limite=500)

                texto = f"[{i}] {titulo}\n{contenido}\nFuente: {url}\n"
                textos.append(texto)

            return TokenManager.recortar_texto("\n".join(textos), limite=LIMITE_TOTAL)

        except Exception as e:
            logger.error(f"Error extrayendo contenido: {e}")
            return ""


def verificar_tavily() -> bool:
    """
    Verifica que Tavily esté disponible.
    Útil para UI o verificación inicial.
    """
    try:
        cliente = TavilyClientWrapper()
        resultados = cliente.buscar("test", max_results=1)
        return True
    except Exception:
        return False