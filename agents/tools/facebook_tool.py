"""
Tool para formatear contenido para Facebook.
"""

import logging

logger = logging.getLogger(__name__)

def facebook_tool(contenido: str) -> dict:
    """
    Formatea el contenido para Facebook.
    Retorna el contenido completo (incluye hashtags).
    """
    logger.info("👍 Usando Facebook Tool")
    
    # Parsear el contenido de entrada
    lineas = contenido.strip().split('\n')
    titulo = ""
    cuerpo = ""
    cta = ""
    keywords = []
    
    for linea in lineas:
        if linea.startswith('TÍTULO:'):
            titulo = linea.replace('TÍTULO:', '').strip()
        elif linea.startswith('CONTENIDO:'):
            cuerpo = linea.replace('CONTENIDO:', '').strip()
        elif linea.startswith('CTA:'):
            cta = linea.replace('CTA:', '').strip()
        elif linea.startswith('KEYWORDS:'):
            keywords_texto = linea.replace('KEYWORDS:', '').strip()
            keywords = [k.strip() for k in keywords_texto.split(',') if k.strip()]
    
    # Valores por defecto
    if not titulo:
        titulo = "Comparto esto con mi comunidad"
    if not cuerpo:
        cuerpo = "Un tema para conversar en familia."
    if not cta:
        cta = "Comparte tu opinión"
    if not keywords:
        keywords = ["comunidad", "familia", "compartir"]
    
    # Formato conversacional para Facebook
    cuerpo_facebook = f"📌 {titulo}\n\n{cuerpo}"
    
    # Párrafos
    if '\n' not in cuerpo_facebook:
        cuerpo_facebook = cuerpo_facebook.replace('. ', '.\n\n')
    
    # CTA para comunidad
    cta_facebook = f"\n\n{cta}\n\nComparte tu opinión 👇"
    
    # Hashtags moderados (máximo 3)
    hashtags = [f"#{k.replace(' ', '')}" for k in keywords[:3]]
    hashtags_facebook = " ".join(hashtags)
    
    # Contenido completo (YA INCLUYE HASHTAGS)
    contenido_completo = f"{cuerpo_facebook}{cta_facebook}\n\n{hashtags_facebook}"
    
    return {
        "red_social": "facebook",
        "contenido": contenido_completo,  # Esto ya tiene todo
        "titulo": titulo,
        "hashtags": hashtags,              # Solo para referencia
        "icono": "👍"
    }