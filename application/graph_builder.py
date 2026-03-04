"""
Construcción del grafo multi-agente con branching avanzado.
"""

from langgraph.graph import StateGraph, START, END

from domain.state import EstadoContenido
from agents.router_agent import router_agent
from agents.linkedin_agent import linkedin_agent
from agents.instagram_agent import instagram_agent
from agents.product_agent import product_agent
from agents.optimizer_agent import optimizer_agent


def decidir_ruta(state: EstadoContenido) -> str:
    """
    Decide el siguiente nodo según tipo de contenido o red social.
    """
    tipo = state.get("tipo_contenido", "")
    red = state.get("red_social", "")

    if tipo == "producto":
        return "product"

    if red == "linkedin":
        return "linkedin"

    if red == "instagram":
        return "instagram"

    return END


def construir_grafo():
    """
    Construye y compila el grafo principal.
    """
    builder = StateGraph(EstadoContenido)

    # Nodos
    builder.add_node("router", router_agent)
    builder.add_node("linkedin", linkedin_agent)
    builder.add_node("instagram", instagram_agent)
    builder.add_node("product", product_agent)
    builder.add_node("optimizer", optimizer_agent)

    # Flujo inicial
    builder.add_edge(START, "router")

    # Branching principal
    builder.add_conditional_edges(
        "router",
        decidir_ruta,
        {
            "linkedin": "linkedin",
            "instagram": "instagram",
            "product": "product",
            END: END,
        },
    )

    # Optimización después de generación
    builder.add_edge("linkedin", "optimizer")
    builder.add_edge("instagram", "optimizer")
    builder.add_edge("product", "optimizer")

    builder.add_edge("optimizer", END)

    return builder.compile()