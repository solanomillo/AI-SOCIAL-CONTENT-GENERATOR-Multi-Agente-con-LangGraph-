"""
Construcción del grafo con agente unificado.
"""

from langgraph.graph import StateGraph, START, END
from domain.state import EstadoContenido
from agents.unified_agent import unified_agent

import logging

logger = logging.getLogger(__name__)


def construir_grafo():
    """
    Grafo con un solo nodo que hace todo.
    """
    logger.info("🔄 Construyendo grafo...")
    
    builder = StateGraph(EstadoContenido)

    # Un solo nodo
    builder.add_node("unified", unified_agent)

    # Flujo directo
    builder.add_edge(START, "unified")
    builder.add_edge("unified", END)

    logger.info("✅ Grafo construido")
    return builder.compile()