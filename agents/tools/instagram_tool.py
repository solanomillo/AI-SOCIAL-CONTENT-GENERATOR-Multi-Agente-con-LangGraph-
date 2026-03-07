"""
Tool para formatear contenido para Instagram.
"""

import logging

logger = logging.getLogger(__name__)

def instagram_tool(contenido: str) -> dict:
    """
    Formatea el contenido para Instagram.
    Retorna el contenido completo (incluye hashtags).
    """
    logger.info("📸 Usando Instagram Tool")
    
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
        titulo = "¡Descubre esta experiencia única!"
    if not cuerpo:
        cuerpo = "Un lugar especial que tienes que conocer."
    if not cta:
        cta = "Guarda este post para tu próxima visita"
    if not keywords:
        keywords = ["experiencia", "unica", "descubre"]
    
    # Formatear título para Instagram
    titulo_instagram = f"✨ {titulo} ✨"
    
    # Formatear cuerpo
    if '\n' in cuerpo:
        parrafos = cuerpo.split('\n')
        cuerpo_instagram = '\n\n'.join(parrafos)
    else:
        # Dividir en frases
        frases = cuerpo.split('. ')
        cuerpo_instagram = '.\n\n'.join(frases)
    
    # CTA para Instagram
    cta_instagram = f"\n\n{cta}\n👇 Cuéntanos en los comentarios 👇"
    
    # Hashtags (máximo 8)
    hashtags = [f"#{k.replace(' ', '')}" for k in keywords[:8]]
    hashtags_instagram = " ".join(hashtags)
    
    # Contenido completo (YA INCLUYE HASHTAGS)
    contenido_completo = f"{titulo_instagram}\n\n{cuerpo_instagram}{cta_instagram}\n\n{hashtags_instagram}"
    
    return {
        "red_social": "instagram",
        "contenido": contenido_completo,  # Esto ya tiene todo
        "titulo": titulo_instagram,
        "hashtags": hashtags,              # Solo para referencia
        "icono": "📸"
    }