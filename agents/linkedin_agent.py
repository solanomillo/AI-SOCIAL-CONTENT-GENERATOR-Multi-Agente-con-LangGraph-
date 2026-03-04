"""
Agente especializado en generación de contenido para LinkedIn.

Responsabilidad:
- Generar posts profesionales optimizados.
- Aplicar framework de marketing seleccionado.
- Incluir CTA estratégico.
"""

from domain.state import EstadoContenido
from infrastructure.gemini_client import ClienteGemini


def linkedin_agent(state: EstadoContenido) -> EstadoContenido:
    """
    Genera contenido optimizado para LinkedIn.

    Args:
        state (EstadoContenido): Estado actual del grafo.

    Returns:
        EstadoContenido: Estado actualizado con el resultado generado.
    """
    cliente = ClienteGemini()

    prompt = f"""
    Genera un post profesional para LinkedIn.

    Tema: {state['prompt_usuario']}
    Framework: {state['framework']}
    Tono: {state['tono']}

    Reglas:
    - Usa un hook fuerte en la primera línea.
    - Usa espacios entre párrafos.
    - Incluye un CTA profesional al final.
    - Máximo 200 palabras.
    """

    respuesta = cliente.generar(prompt)

    state["resultado"] = respuesta

    return state