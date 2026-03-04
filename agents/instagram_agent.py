"""
Agente especializado en generación de contenido para Instagram.

Responsabilidad:
- Generar contenido emocional o visual.
- Incluir hashtags estratégicos.
- Aplicar framework de marketing.
"""

from domain.state import EstadoContenido
from infrastructure.gemini_client import ClienteGemini


def instagram_agent(state: EstadoContenido) -> EstadoContenido:
    """
    Genera contenido optimizado para Instagram.

    Args:
        state (EstadoContenido): Estado actual del grafo.

    Returns:
        EstadoContenido: Estado actualizado con resultado generado.
    """
    cliente = ClienteGemini()

    prompt = f"""
    Genera un post optimizado para Instagram.

    Tema: {state['prompt_usuario']}
    Framework: {state['framework']}
    Tono: {state['tono']}

    Reglas:
    - Primera línea debe ser impactante.
    - Usar estilo emocional o visual.
    - Incluir emojis moderados.
    - Incluir entre 5 y 8 hashtags relevantes al final.
    - Incluir CTA claro y corto.
    - Máximo 150 palabras.
    """

    respuesta = cliente.generar(prompt)

    state["resultado"] = respuesta

    return state