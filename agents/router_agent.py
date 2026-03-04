"""
Agente Router.
Decide qué tipo de contenido generar y cómo procesarlo.
"""

import json
import re
from domain.state import EstadoContenido
from domain.models import DecisionRouter
from infrastructure.gemini_client import ClienteGemini


def extraer_json(texto: str) -> str:
    """
    Extrae el primer bloque JSON válido desde un string.
    Maneja casos donde el LLM devuelve markdown o texto adicional.
    """
    if not texto:
        raise ValueError("La respuesta del modelo está vacía.")

    texto = texto.strip()

    # Elimina bloques ```json ```
    if texto.startswith("```"):
        bloques = re.findall(r"```(?:json)?(.*?)```", texto, re.DOTALL)
        if bloques:
            texto = bloques[0].strip()

    # Extrae el JSON entre llaves si hay texto adicional
    match = re.search(r"\{.*\}", texto, re.DOTALL)
    if match:
        return match.group()

    return texto


def router_agent(state: EstadoContenido) -> EstadoContenido:
    cliente = ClienteGemini()

    prompt = f"""
    Analiza el siguiente pedido de contenido:

    "{state['prompt_usuario']}"

    Devuelve una respuesta en formato JSON con las siguientes claves:
    - tipo_contenido (post, producto, carrusel)
    - red_social (linkedin, instagram, twitter)
    - framework (AIDA, PAS, Storytelling)
    - tono (profesional, emocional, tecnico, persuasivo)
    - requiere_investigacion (true o false)

    SOLO responde el JSON válido.
    """

    respuesta = cliente.generar(prompt)

    try:
        # DEBUG opcional (podés quitarlo después)
        print("RESPUESTA CRUDA:", repr(respuesta))

        json_limpio = extraer_json(respuesta)
        data = json.loads(json_limpio)

        decision = DecisionRouter(**data)

        state.update({
            "tipo_contenido": decision.tipo_contenido,
            "red_social": decision.red_social,
            "framework": decision.framework,
            "tono": decision.tono,
            "requiere_investigacion": decision.requiere_investigacion,
        })

    except json.JSONDecodeError:
        state["resultado"] = "El modelo no devolvió un JSON válido."
    except ValueError as e:
        state["resultado"] = f"Error: {str(e)}"
    except Exception as e:
        state["resultado"] = f"Error procesando router: {str(e)}"

    return state