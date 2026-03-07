"""
Tool para formatear contenido para LinkedIn.
"""

import logging

logger = logging.getLogger(__name__)

def linkedin_tool(contenido: str) -> dict:
    """
    Formatea el contenido para LinkedIn.
    Retorna el contenido completo (incluye hashtags).
    """
    logger.info("💼 Usando LinkedIn Tool")
    
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
        titulo = "Comparto esta reflexión profesional"
    if not cuerpo:
        cuerpo = "Un tema relevante para nuestra red profesional."
    if not cta:
        cta = "Comparte tu opinión en los comentarios"
    if not keywords:
        keywords = ["profesional", "carrera", "desarrollo"]
    
    # Formatear título para LinkedIn
    titulo_linkedin = f"**{titulo}**"
    
    # Formatear cuerpo en párrafos cortos
    if '\n' in cuerpo:
        parrafos = cuerpo.split('\n')
    else:
        parrafos = [p.strip() + '.' for p in cuerpo.split('.') if p.strip()]
    cuerpo_linkedin = '\n\n'.join(parrafos)
    
    # CTA profesional
    cta_linkedin = f"\n\n{cta}\n\n¿Qué opinas? Te leo en comentarios."
    
    # Hashtags profesionales (máximo 6)
    hashtags = [f"#{k.replace(' ', '')}" for k in keywords[:6]]
    hashtags_linkedin = " ".join(hashtags)
    
    # Contenido completo (YA INCLUYE HASHTAGS)
    contenido_completo = f"{titulo_linkedin}\n\n{cuerpo_linkedin}{cta_linkedin}\n\n{hashtags_linkedin}"
    
    return {
        "red_social": "linkedin",
        "contenido": contenido_completo,  # Esto ya tiene todo
        "titulo": titulo,
        "hashtags": hashtags,              # Solo para referencia
        "icono": "💼"
    }