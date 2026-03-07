"""
Unified Agent - Flujo lineal y claro.
1. Genera contenido base
2. Router decide red social
3. Tool formatea
"""

import logging
import time
import re
from domain.state import EstadoContenido
from domain.models import Producto, DecisionRouter, PostGenerado
from infrastructure.gemini_client import ClienteGemini
from infrastructure.tavily_client import TavilyClientWrapper
from agents.router_agent import router_agent, aplicar_tool

logger = logging.getLogger(__name__)

UNIFIED_PROMPT = """
Eres un copywriter experto en marketing digital.

Basado en esta idea: "{idea}"

{investigacion}

Genera un contenido atractivo y persuasivo con este formato EXACTO:

TÍTULO: [título llamativo - máximo 10 palabras]
CONTENIDO: [texto principal - 3 a 5 párrafos cortos]
CTA: [llamado a la acción - 1 frase]
KEYWORDS: [palabra1, palabra2, palabra3, palabra4, palabra5]

REGLAS:
- No incluyas texto adicional
- Respeta el formato exacto
- Las keywords serán usadas para hashtags
"""


def parsear_contenido_base(texto: str) -> dict:
    """
    Parsea la respuesta de Gemini para extraer título, contenido, CTA y keywords.
    """
    resultado = {
        "titulo": "",
        "contenido": "",
        "cta": "",
        "keywords": []
    }
    
    lineas = texto.strip().split('\n')
    seccion_actual = None
    contenido_temp = []
    
    for linea in lineas:
        linea = linea.strip()
        if not linea:
            continue
            
        if linea.startswith('TÍTULO:'):
            resultado["titulo"] = linea.replace('TÍTULO:', '').strip()
            seccion_actual = "titulo"
        elif linea.startswith('CONTENIDO:'):
            seccion_actual = "contenido"
            contenido_temp = []
        elif linea.startswith('CTA:'):
            if contenido_temp:
                resultado["contenido"] = '\n'.join(contenido_temp)
            resultado["cta"] = linea.replace('CTA:', '').strip()
            seccion_actual = "cta"
        elif linea.startswith('KEYWORDS:'):
            keywords_texto = linea.replace('KEYWORDS:', '').strip()
            resultado["keywords"] = [k.strip() for k in keywords_texto.split(',') if k.strip()]
            seccion_actual = "keywords"
        elif seccion_actual == "contenido":
            contenido_temp.append(linea)
    
    # Si el contenido no se guardó, guardarlo ahora
    if contenido_temp and not resultado["contenido"]:
        resultado["contenido"] = '\n'.join(contenido_temp)
    
    # Valores por defecto
    if not resultado["titulo"]:
        resultado["titulo"] = "Descubre esta oportunidad"
    if not resultado["contenido"]:
        resultado["contenido"] = texto
    if not resultado["cta"]:
        resultado["cta"] = "Conoce más información"
    if not resultado["keywords"]:
        resultado["keywords"] = ["marketing", "contenido", "redes"]
    
    return resultado


def unified_agent(state: EstadoContenido) -> EstadoContenido:
    """
    Flujo lineal: 1. Generar base → 2. Router → 3. Tool → 4. Guardar
    """
    logger.info("🚀 Unified agent iniciado")
    state["tiempo_inicio"] = time.time()

    try:
        idea = state.get("prompt_usuario")
        if not idea:
            state["error"] = "No hay descripción"
            return state

        # =========================
        # 1. INVESTIGACIÓN (opcional)
        # =========================
        investigacion_texto = ""
        if state.get("forzar_investigacion", False):
            logger.info("🔍 Investigando con Tavily...")
            try:
                tavily = TavilyClientWrapper()
                resultados = tavily.buscar(idea, max_results=3)
                if resultados:
                    texto = tavily.extraer_contenido(resultados)
                    if texto and len(texto) > 50:
                        investigacion_texto = f"\nDatos de investigación:\n{texto}\n"
                        logger.info(f"✅ Investigación: {len(texto)} caracteres")
            except Exception as e:
                logger.warning(f"⚠️ Error en Tavily: {e}")

        # =========================
        # 2. GENERAR CONTENIDO BASE
        # =========================
        prompt = UNIFIED_PROMPT.format(
            idea=idea,
            investigacion=investigacion_texto
        )

        cliente = ClienteGemini(temperature=0.7)
        logger.info("📤 Generando contenido base...")
        respuesta = cliente.generar_texto(prompt)
        
        logger.info(f"✅ Respuesta recibida: {len(respuesta)} caracteres")
        
        # Parsear la respuesta
        contenido_parseado = parsear_contenido_base(respuesta)
        
        titulo = contenido_parseado["titulo"]
        contenido = contenido_parseado["contenido"]
        cta = contenido_parseado["cta"]
        keywords = contenido_parseado["keywords"]

        logger.info(f"📋 Título: {titulo}")
        logger.info(f"📋 Keywords: {keywords}")

        # =========================
        # 3. PREPARAR INPUT PARA ROUTER
        # =========================
        input_router = f"{titulo}\n\n{contenido}\n\nCTA: {cta}\n\nKeywords: {', '.join(keywords)}"
        
        # =========================
        # 4. ROUTER DECIDE RED SOCIAL
        # =========================
        red_social = router_agent(input_router)
        logger.info(f"🎯 Red social elegida: {red_social}")

        # =========================
        # 5. APLICAR TOOL CORRESPONDIENTE
        # =========================
        contenido_completo = (
            f"TÍTULO: {titulo}\n"
            f"CONTENIDO: {contenido}\n"
            f"CTA: {cta}\n"
            f"KEYWORDS: {', '.join(keywords)}"
        )
        
        resultado_tool = aplicar_tool(red_social, contenido_completo)
        
        # =========================
        # 6. CREAR OBJETOS DEL DOMINIO
        # =========================
        state["producto"] = Producto(
            nombre=idea[:30],
            descripcion=idea,
            caracteristicas=[],
            beneficios=[]
        )
        
        decision = DecisionRouter(
            tipo_contenido="promocional",
            red_social=red_social,
            framework="PAS",
            tono="profesional",
            requiere_investigacion=bool(investigacion_texto)
        )
        state["decision_router"] = decision
        state["red_social"] = red_social
        
        # Post generado
        state["post_generado"] = PostGenerado(
            titulo=resultado_tool.get("titulo", titulo),
            contenido=resultado_tool.get("contenido", contenido),
            hashtags=resultado_tool.get("hashtags", [f"#{k}" for k in keywords[:5]]),
            red_social=red_social
        )

        # Texto para UI
        state["estrategia_texto"] = f"Red Social: {red_social}"

        logger.info(f"✅ Proceso completado para {red_social}")

    except Exception as e:
        logger.exception("❌ Error en unified_agent")
        state["error"] = f"Error: {str(e)}"

    return state