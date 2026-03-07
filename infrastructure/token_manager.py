"""
Gestión de tamaño de prompts para evitar exceder límites de tokens.
Herramienta simple y eficiente para recortar textos.
"""

import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)


class TokenManager:
    """
    Controla el tamaño del contexto enviado al modelo.
    """

    # Límite global por defecto (caracteres, no tokens)
    MAX_PROMPT_CHARS = 12000

    # Límites por tipo de agente (para mayor control)
    LIMITES_POR_AGENTE = {
        "product": 8000,
        "router": 6000,
        "research": 10000,
        "instagram": 8000,
        "linkedin": 8000,
        "optimizer": 4000,
    }

    @staticmethod
    def recortar_texto(
        texto: Optional[str], 
        limite: Optional[int] = None,
        agente: Optional[str] = None
    ) -> Optional[str]:
        """
        Recorta un texto si excede el límite especificado.
        
        Args:
            texto: Texto a recortar
            limite: Límite en caracteres (opcional)
            agente: Nombre del agente (usa límite específico si existe)
            
        Returns:
            Texto recortado o None si el input era None
        """
        if not texto:
            return texto

        # Determinar límite
        max_chars = limite
        if not max_chars and agente:
            max_chars = TokenManager.LIMITES_POR_AGENTE.get(agente)
        if not max_chars:
            max_chars = TokenManager.MAX_PROMPT_CHARS

        # Recortar si es necesario
        if len(texto) > max_chars:
            logger.debug(f"✂️ Texto recortado: {len(texto)} → {max_chars} chars")
            return texto[:max_chars]

        return texto

    @staticmethod
    def estimar_tokens(texto: Optional[str]) -> int:
        """
        Estimación rápida de tokens (4 caracteres ≈ 1 token).
        Útil para logging.
        """
        if not texto:
            return 0
        return max(1, len(texto) // 4)

    @staticmethod
    def estadisticas(texto: Optional[str], nombre: str = "texto") -> Dict[str, Any]:
        """
        Obtiene estadísticas básicas del texto.
        """
        if not texto:
            return {
                "nombre": nombre,
                "caracteres": 0,
                "tokens_estimados": 0,
                "palabras": 0,
                "esta_vacio": True
            }

        return {
            "nombre": nombre,
            "caracteres": len(texto),
            "tokens_estimados": len(texto) // 4,
            "palabras": len(texto.split()),
            "esta_vacio": False
        }


# =========================
# FUNCIONES DE AYUDA (para uso directo)
# =========================

def recortar(texto: Optional[str], max_chars: int = 500) -> str:
    """
    Función rápida para recortar textos en una línea.
    Útil para logging y debugging.
    """
    if not texto:
        return ""
    if len(texto) <= max_chars:
        return texto
    return texto[:max_chars] + "..."


def primer_parrafo(texto: Optional[str], max_chars: int = 200) -> str:
    """
    Extrae el primer párrafo de un texto.
    """
    if not texto:
        return ""
    
    # Buscar primer salto de línea
    if "\n" in texto:
        primer_p = texto.split("\n")[0]
    else:
        primer_p = texto
    
    return recortar(primer_p, max_chars)