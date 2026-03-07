"""
Router Agent - Decide qué red social usar basado en el contenido y preferencia del usuario.
Primero busca menciones explícitas, luego usa Gemini.
"""

import logging
from agents.tools import (
    instagram_tool,
    linkedin_tool,
    tiktok_tool,
    facebook_tool
)
from infrastructure.gemini_client import ClienteGemini

logger = logging.getLogger(__name__)

# Palabras clave para detección rápida
KEYWORDS = {
    "linkedin": [
        "linkedin", "linked in", "linkedin", "profesional", "carrera", 
        "trabajo", "empleo", "curriculum", "b2b", "negocios", "empresa",
        "laboral", "oficina", "corporativo", "cv", "hoja de vida"
    ],
    "instagram": [
        "instagram", "insta", "ig", "foto", "visual", "reels", "historia",
        "fotografía", "imagen", "filtro", "estético", "look", "moda",
        "outfit", "maquillaje", "producto"
    ],
    "tiktok": [
        "tiktok", "tik tok", "viral", "baile", "trend", "challenge",
        "trending", "danza", "coreografía", "reto", "divertido"
    ],
    "facebook": [
        "facebook", "fb", "comunidad", "grupo", "evento", "familiar",
        "familia", "amigos", "discusión", "debate", "compartir"
    ]
}

def detectar_red_por_keywords(contenido: str) -> str | None:
    """
    Detecta si el usuario menciona explícitamente una red social.
    Retorna el nombre de la red o None.
    """
    contenido_lower = contenido.lower()
    
    # Primero buscar menciones directas del nombre de la red
    for red in ["linkedin", "instagram", "tiktok", "facebook"]:
        if red in contenido_lower:
            logger.info(f"🔍 Mención directa detectada: {red}")
            return red
    
    # Luego buscar palabras clave asociadas
    for red, palabras in KEYWORDS.items():
        for palabra in palabras[:5]:  # Solo las más relevantes
            if palabra in contenido_lower:
                logger.info(f"🔍 Palabra clave '{palabra}' sugiere {red}")
                return red
    
    return None

ROUTER_PROMPT = """
Eres un experto en marketing digital. Debes elegir la MEJOR red social para este contenido.

CONTENIDO DEL USUARIO:
"{contenido}"

INSTRUCCIONES:
1. Si el usuario MENCIONA EXPLÍCITAMENTE una red social, USA ESA.
2. Si no, analiza el tipo de contenido y elige la más adecuada.

REDES SOCIALES:
- linkedin: Profesional, carreras, educación, B2B, cursos, artículos
- instagram: Visual, productos, moda, lifestyle, fotos, reels
- tiktok: Viral, entretenimiento, trends, baile, challenges
- facebook: Comunidades, grupos, eventos, discusión familiar

Responde SOLO con JSON:
{
  "red_social": "linkedin",
  "justificacion": "Contenido profesional sobre cursos"
}
"""

def router_agent(contenido: str) -> str:
    """
    Decide qué red social usar.
    Prioridad: 1. Keywords, 2. Gemini, 3. Instagram por defecto.
    """
    logger.info("🤖 Router agent iniciado")
    
    # PASO 1: Detección por keywords
    red_detectada = detectar_red_por_keywords(contenido)
    if red_detectada:
        logger.info(f"✅ Detectada por keywords: {red_detectada}")
        return red_detectada
    
    # PASO 2: Usar Gemini
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
    
    # PASO 3: Default
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