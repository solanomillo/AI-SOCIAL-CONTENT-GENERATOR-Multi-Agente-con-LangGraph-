"""
Tool para formatear contenido para TikTok.
"""

import logging

logger = logging.getLogger(__name__)

def tiktok_tool(contenido: str) -> dict:
    """
    Formatea el contenido para TikTok.
    Retorna el contenido completo (incluye hashtags).
    """
    logger.info("🎵 Usando TikTok Tool")
    
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
        titulo = "¡Esto es viral!"
    if not cuerpo:
        cuerpo = "No te lo puedes perder"
    if not cta:
        cta = "Sígueme para más"
    if not keywords:
        keywords = ["fyp", "viral", "trending"]
    
    # TikTok usa el título como parte del contenido
    cuerpo_tiktok = f"{titulo}\n\n{cuerpo}"
    
    # Acortar si es muy largo
    if len(cuerpo_tiktok) > 200:
        cuerpo_tiktok = cuerpo_tiktok[:197] + "..."
    
    # CTA viral
    cta_tiktok = f"\n\n🔥 {cta} 🔥"
    
    # Hashtags de tendencia (máximo 5)
    hashtags = [f"#{k.replace(' ', '')}" for k in keywords[:5]]
    hashtags_tiktok = " ".join(hashtags)
    
    # Contenido completo (YA INCLUYE HASHTAGS)
    contenido_completo = f"{cuerpo_tiktok}{cta_tiktok}\n\n{hashtags_tiktok}"
    
    return {
        "red_social": "tiktok",
        "contenido": contenido_completo,  # Esto ya tiene todo
        "titulo": titulo,
        "hashtags": hashtags,              # Solo para referencia
        "icono": "🎵"
    }