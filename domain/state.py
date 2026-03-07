"""
Definición del estado compartido del grafo.
Usamos TypedDict para tener type hints claros en LangGraph.
"""

from typing import TypedDict, Optional, List, Dict, Any

from domain.models import (
    DecisionRouter,
    Producto,
    ResultadoInvestigacion,
    PostGenerado,
    PostOptimizado,
)


class EstadoContenido(TypedDict, total=False):
    """
    Estado compartido entre todos los nodos del grafo.
    Todos los campos son opcionales porque no todos los agentes los usan.
    """

    # =========================
    # INPUT DEL USUARIO
    # =========================
    prompt_usuario: str

    # =========================
    # DECISIÓN DEL ROUTER
    # =========================
    decision_router: DecisionRouter
    estrategia_texto: str  # Texto legible para la UI

    # =========================
    # INFORMACIÓN DEL PRODUCTO
    # =========================
    producto: Producto

    # =========================
    # INVESTIGACIÓN (TAVILY)
    # =========================
    investigacion: ResultadoInvestigacion

    # =========================
    # CONTENIDO GENERADO
    # =========================
    post_generado: PostGenerado

    # =========================
    # CONTENIDO OPTIMIZADO
    # =========================
    post_optimizado: PostOptimizado
    datos_optimizacion: Dict[str, Any]  # Datos crudos de optimización

    # =========================
    # METADATOS Y CONTROL
    # =========================
    paso_actual: str
    log_agentes: List[str]
    error: str

    # =========================
    # MÉTRICAS
    # =========================
    tiempo_inicio: float
    tiempo_fin: float