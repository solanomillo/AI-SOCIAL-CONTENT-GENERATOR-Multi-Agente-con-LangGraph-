"""
Router Agent - Decide qué red social usar basado en el contenido y preferencia del usuario.
Primero busca menciones explícitas, luego palabras clave, y finalmente usa Gemini.
"""

import logging
import re
from agents.tools import (
    instagram_tool,
    linkedin_tool,
    tiktok_tool,
    facebook_tool
)
from infrastructure.gemini_client import ClienteGemini

logger = logging.getLogger(__name__)

# Palabras de alta prioridad (menciones explícitas de la red)
REDES_EXPLICITAS = {
    "linkedin": ["linkedin", "linked in", "linkedin"],
    "instagram": ["instagram", "insta", "ig"],
    "tiktok": ["tiktok", "tik tok"],
    "facebook": ["facebook", "fb"]
}

# Palabras clave contextuales (cuando no hay mención explícita)
KEYWORDS = {
    "linkedin": [
        # Contexto profesional
        "profesional", "carrera", "trabajo", "empleo", "curriculum", 
        "b2b", "negocios", "empresa", "corporativo", "laboral", "oficina",
        "puesto", "contratación", "headhunter", "reclutamiento", "industria",
        "experiencia laboral", "networking", "empleo"
    ],
    "instagram": [
        # Contexto visual
        "foto", "visual", "reels", "historia", "fotografía", "imagen", 
        "estético", "look", "moda", "outfit", "maquillaje", "producto",
        "viaje", "paisaje", "comida", "restaurante", "decoración",
        "estilo", "modelo", "photography"
    ],
    "tiktok": [
        # Contexto viral
        "viral", "baile", "trend", "challenge", "trending", "danza", 
        "coreografía", "reto", "divertido", "humor", "gracioso", "entretenimiento",
        "funny", "comedia", "sketch", "actuación"
    ],
    "facebook": [
        # Contexto comunitario
        "comunidad", "grupo", "evento", "familiar", "familia", "amigos", 
        "discusión", "debate", "compartir", "cumpleaños", "reunión",
        "vecinos", "local", "comunitario", "grupo de ayuda", "citas"
    ]
}

def detectar_red_por_keywords(contenido: str) -> str | None:
    """
    Detecta si el usuario menciona explícitamente una red social.
    Prioridad 1: Menciones directas de la red
    Prioridad 2: Palabras clave contextuales
    """
    contenido_lower = contenido.lower()
    
    # PRIORIDAD 1: Buscar menciones DIRECTAS del nombre de la red
    for red, palabras in REDES_EXPLICITAS.items():
        for palabra in palabras:
            # Buscar la palabra como término independiente o con preposición
            patrones = [
                rf'\b{palabra}\b',                 # palabra exacta
                rf'para {palabra}',                 # "para instagram"
                rf'en {palabra}',                    # "en instagram"
                rf'de {palabra}',                    # "de instagram"
                rf'a {palabra}',                      # "a instagram"
                rf'por {palabra}',                    # "por instagram"
                rf'mediante {palabra}',               # "mediante instagram"
                rf'usando {palabra}',                 # "usando instagram"
                rf'publicar en {palabra}',            # "publicar en instagram"
                rf'subir a {palabra}',                # "subir a instagram"
                rf'post para {palabra}',              # "post para instagram"
                rf'contenido para {palabra}',         # "contenido para instagram"
            ]
            for patron in patrones:
                if re.search(patron, contenido_lower):
                    logger.info(f"🔍 Mención EXPLÍCITA detectada: {red} (patrón: {patron})")
                    return red
    
    # PRIORIDAD 2: Buscar palabras clave contextuales
    for red, palabras in KEYWORDS.items():
        for palabra in palabras[:5]:  # Solo las más relevantes
            if palabra in contenido_lower:
                logger.info(f"🔍 Palabra clave contextual '{palabra}' sugiere {red}")
                return red
    
    return None


ROUTER_PROMPT = """
Eres un experto en marketing digital. Debes elegir la MEJOR red social para este contenido.

CONTENIDO DEL USUARIO:
"{contenido}"

INSTRUCCIONES IMPORTANTES:
1. Si el usuario MENCIONA EXPLÍCITAMENTE una red social (linkedin, instagram, tiktok, facebook), USA ESA.
   Ejemplos: "para LinkedIn", "en Instagram", "post para TikTok", "compartir en Facebook", "subir a IG"

2. Si no hay mención explícita, analiza el tipo de contenido y elige la más adecuada:
   - linkedin: Contenido profesional, carreras, educación, B2B, cursos, experiencia laboral
   - instagram: Contenido visual, moda, viajes, comida, productos, fotografía
   - tiktok: Contenido viral, entretenimiento, baile, trends, humor, challenges
   - facebook: Comunidades, eventos, grupos, contenido familiar, discusiones

Responde SOLO con JSON en este formato:
{
  "red_social": "linkedin",
  "justificacion": "explicación breve de la decisión"
}
"""


def router_agent(contenido: str) -> str:
    """
    Decide qué red social usar.
    Prioridad: 1. Menciones explícitas, 2. Keywords, 3. Gemini, 4. Instagram por defecto.
    """
    logger.info("🤖 Router agent iniciado")
    
    # PASO 1: Detección por menciones explícitas y keywords
    red_detectada = detectar_red_por_keywords(contenido)
    if red_detectada:
        logger.info(f"✅ Detectada por reglas: {red_detectada}")
        return red_detectada
    
    # PASO 2: Usar Gemini si no hay detección clara
    try:
        contenido_recortado = contenido[:800]
        prompt = ROUTER_PROMPT.format(contenido=contenido_recortado)
        
        cliente = ClienteGemini(temperature=0.2)
        data = cliente.generar_json(prompt)
        
        if data and "red_social" in data:
            red_social = data["red_social"].lower().strip()
            justificacion = data.get("justificacion", "")
            
            # Validar red
            if red_social in ["linkedin", "instagram", "tiktok", "facebook"]:
                logger.info(f"✅ Gemini eligió: {red_social} - {justificacion[:50]}")
                return red_social
            else:
                logger.warning(f"Gemini devolvió red inválida: {red_social}")
    
    except Exception as e:
        logger.error(f"❌ Error en Gemini: {e}")
    
    # PASO 3: Default (Instagram)
    logger.info("⚠️ Usando Instagram por defecto")
    return "instagram"


def aplicar_tool(red_social: str, contenido_base: str) -> dict:
    """
    Aplica la herramienta correspondiente.
    """
    tools = {
        "instagram": instagram_tool,
        "linkedin": linkedin_tool,
        "tiktok": tiktok_tool,
        "facebook": facebook_tool
    }
    
    tool = tools.get(red_social, instagram_tool)
    logger.info(f"🎨 Formateando para {red_social}")
    
    try:
        return tool(contenido_base)
    except Exception as e:
        logger.error(f"❌ Error en tool {red_social}: {e}")
        return instagram_tool(contenido_base)