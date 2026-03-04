"""
Agente optimizador de contenido.

Responsabilidad:
- Mejorar claridad.
- Aumentar persuasión.
- Fortalecer CTA.
"""

from domain.state import EstadoContenido
from infrastructure.gemini_client import ClienteGemini


def optimizer_agent(state: EstadoContenido) -> EstadoContenido:
    """
    Mejora el contenido generado previamente.

    Args:
        state (EstadoContenido): Estado actual del grafo.

    Returns:
        EstadoContenido: Estado optimizado.
    """
    if not state.get("resultado"):
        return state

    cliente = ClienteGemini()

    prompt = f"""
    Optimiza el siguiente contenido:

    {state['resultado']}

    Mejora:
    - Claridad
    - Fluidez
    - Fuerza del CTA
    - Impacto emocional

    No expliques cambios.
    Devuelve solo el contenido mejorado.
    """

    respuesta = cliente.generar(prompt)

    state["resultado"] = respuesta

    return state