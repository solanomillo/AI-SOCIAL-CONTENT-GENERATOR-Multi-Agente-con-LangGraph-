"""
Estado global del sistema multi-agente.
Define qué información viaja entre nodos del grafo.
"""

from typing import Optional, TypedDict


class EstadoContenido(TypedDict):
    prompt_usuario: str
    tipo_contenido: Optional[str]
    red_social: Optional[str]
    framework: Optional[str]
    tono: Optional[str]
    requiere_investigacion: Optional[bool]
    resultado: Optional[str]