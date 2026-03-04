"""
Agente especializado en generación de contenido para productos.

Responsabilidad:
- Crear copy persuasivo.
- Aplicar frameworks de marketing.
- Enfocarse en beneficios > características.
"""

from domain.state import EstadoContenido
from infrastructure.gemini_client import ClienteGemini


def product_agent(state: EstadoContenido) -> EstadoContenido:
    """
    Genera copy de venta para un producto o servicio.

    Args:
        state (EstadoContenido): Estado actual del grafo.

    Returns:
        EstadoContenido: Estado actualizado con el copy generado.
    """
    cliente = ClienteGemini()

    prompt = f"""
    Genera un copy persuasivo para vender un producto o servicio.

    Descripción: {state['prompt_usuario']}
    Framework: {state['framework']}
    Tono: {state['tono']}

    Reglas:
    - Enfócate en beneficios antes que características.
    - Genera urgencia moderada.
    - Incluye un CTA claro.
    - Máximo 180 palabras.
    """

    respuesta = cliente.generar(prompt)

    state["resultado"] = respuesta

    return state