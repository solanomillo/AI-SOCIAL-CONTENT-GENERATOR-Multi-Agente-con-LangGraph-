"""
Interfaz principal con Streamlit.
Diseño profesional con agente unificado y soporte para múltiples redes sociales.
Versión con botón copiar simple y funcional.
"""

import streamlit as st
import asyncio
import time
import logging
from application.graph_builder import construir_grafo
from infrastructure.gemini_client import verificar_cuota

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_app():
    """Función principal de la aplicación."""

    st.set_page_config(
        page_title="AI Social Content Generator",
        page_icon="⚡",
        layout="centered",
        initial_sidebar_state="collapsed"
    )

    # CSS personalizado
    st.markdown("""
        <style>
        /* Tipografía general */
        .stApp {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
        }
        
        /* Títulos principales */
        h1 {
            font-size: 2.2rem !important;
            font-weight: 600 !important;
            letter-spacing: -0.02em !important;
            margin-bottom: 0.5rem !important;
            color: #1E1E1E !important;
        }
        
        /* Cápsula de versión */
        .version-badge {
            display: inline-block;
            background: #E8F0FE;
            color: #0066CC;
            font-size: 0.7rem;
            font-weight: 500;
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            margin-left: 0.5rem;
            vertical-align: middle;
        }
        
        /* Subtítulos */
        h2, h3, h4, h5, h6 {
            font-weight: 500 !important;
            color: #333 !important;
        }
        
        /* Texto del expander */
        .streamlit-expanderHeader {
            font-size: 0.9rem !important;
            font-weight: 400 !important;
            color: #666 !important;
        }
        
        .streamlit-expanderContent {
            font-size: 0.85rem !important;
            line-height: 1.5 !important;
            color: #4A4A4A !important;
        }
        
        /* Área de texto */
        .stTextArea textarea {
            font-size: 0.95rem !important;
            border: 1px solid #E0E0E0 !important;
            border-radius: 8px !important;
        }
        
        /* Botón principal */
        .stButton button {
            font-size: 1rem !important;
            font-weight: 500 !important;
            padding: 0.5rem 2rem !important;
            border-radius: 8px !important;
            background: #0066CC !important;
            color: white !important;
            border: none !important;
            transition: all 0.2s ease;
        }
        
        .stButton button:hover {
            background: #0052A3 !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        
        .stButton button:active {
            transform: translateY(0);
        }
        
        /* Botón secundario */
        .stButton button[kind="secondary"] {
            background: white !important;
            color: #0066CC !important;
            border: 1px solid #0066CC !important;
        }
        
        .stButton button[kind="secondary"]:hover {
            background: #F0F7FF !important;
        }
        
        /* Métricas */
        div[data-testid="stMetric"] {
            background: #F8F9FA !important;
            padding: 1rem !important;
            border-radius: 8px !important;
            border: 1px solid #E0E0E0 !important;
            min-height: 100px !important;
            transition: all 0.2s ease;
        }
        
        div[data-testid="stMetric"]:hover {
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        
        div[data-testid="stMetric"] label {
            font-size: 0.8rem !important;
            color: #666 !important;
            display: block !important;
            margin-bottom: 0.5rem !important;
        }
        
        div[data-testid="stMetric"] [data-testid="stMetricValue"] {
            font-size: 1.2rem !important;
            font-weight: 600 !important;
            color: #0066CC !important;
            display: block !important;
        }
        
        /* Contenido generado */
        .generated-content {
            background: #F8F9FA;
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid #E0E0E0;
            margin: 1rem 0;
            color: #333 !important;
            line-height: 1.6;
        }
        
        .generated-content h3 {
            margin-top: 0 !important;
            margin-bottom: 1rem !important;
            color: #0066CC !important;
        }
        
        .generated-content p {
            margin-bottom: 0.8rem;
        }
        
        /* Badges para redes sociales */
        .social-badge {
            display: inline-block;
            padding: 0.3rem 1rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .instagram-badge {
            background: linear-gradient(45deg, #f09433, #d62976, #962fbf);
            color: white;
        }
        
        .linkedin-badge {
            background: #0077b5;
            color: white;
        }
        
        .tiktok-badge {
            background: #000000;
            color: white;
        }
        
        .facebook-badge {
            background: #4267B2;
            color: white;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            color: #999;
            font-size: 0.8rem;
            margin-top: 3rem;
            padding-top: 2rem;
            border-top: 1px solid #E0E0E0;
        }
        </style>
    """, unsafe_allow_html=True)

    # =========================
    # HEADER
    # =========================
    st.markdown("""
        <h1>
            ⚡ AI Social Content Generator
            <span class="version-badge">Multi-Red v2.0</span>
        </h1>
    """, unsafe_allow_html=True)
    
    st.caption("Instagram · LinkedIn · TikTok · Facebook · 2 llamadas a Gemini")

    # =========================
    # CÓMO FUNCIONA
    # =========================
    with st.expander("ℹ️ Cómo funciona"):
        st.markdown("""
        **1. Análisis** · Extrae información clave de tu idea  
        **2. Investigación** · Busca tendencias relevantes (opcional)  
        **3. Decisión** · IA elige la mejor red social para tu contenido  
        **4. Generación** · Crea el post optimizado para la red elegida
        """)

    st.divider()

    # =========================
    # INPUT PRINCIPAL
    # =========================
    st.markdown("##### 📝 Describe tu idea")
    
    user_input = st.text_area(
        label="Descripción del contenido",
        placeholder="Ej: Curso de Python para principiantes. También aceptamos ideas para LinkedIn, TikTok o Facebook!",
        height=120,
        label_visibility="collapsed",
        key="input_idea"
    )

    # Checkbox para investigación
    col1, col2 = st.columns([1, 3])
    with col1:
        investigar = st.checkbox("🔍 Investigar tendencias", value=True, 
                                help="Busca información relevante en internet para mejorar el contenido")
    with col2:
        st.markdown("")  # Espaciado

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generar = st.button("✨ Generar contenido", type="primary", use_container_width=True)

    st.divider()

    # =========================
    # GENERACIÓN
    # =========================
    if generar:
        if not user_input.strip():
            st.warning("Por favor escribe una descripción")
            return

        # Verificar cuota
        with st.spinner("Verificando API..."):
            cuota_disponible = verificar_cuota()

        if not cuota_disponible:
            st.error("### Límite de API alcanzado")
            st.info("""
            Has llegado al límite gratuito de Gemini (5 requests por minuto).  
            La cuota se restablece cada 60 minutos.
            """)
            
            if st.button("🔄 Reintentar", type="secondary"):
                st.rerun()
            return

        # Inicializar grafo
        if "grafo" not in st.session_state:
            with st.spinner("Inicializando sistema..."):
                st.session_state.grafo = construir_grafo()

        # Estado inicial
        estado_inicial = {
            "prompt_usuario": user_input,
            "forzar_investigacion": investigar,
            "decision_router": None,
            "producto": None,
            "investigacion": None,
            "post_generado": None,
            "post_optimizado": None,
            "datos_optimizacion": None,
            "paso_actual": None,
            "log_agentes": [],
            "error": None,
            "tiempo_inicio": time.time()
        }

        # Inicializar variable resultado
        resultado = None
        
        # Barra de progreso
        progress_bar = st.progress(0, text="Iniciando...")

        try:
            with st.spinner(""):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                progress_bar.progress(30, text="Analizando tu idea...")
                resultado = loop.run_until_complete(
                    st.session_state.grafo.ainvoke(estado_inicial)
                )
                progress_bar.progress(80, text="Generando contenido...")
                loop.close()

            progress_bar.progress(100, text="¡Listo!")
            time.sleep(0.3)
            progress_bar.empty()

        except Exception as e:
            st.error(f"❌ Error en la generación: {str(e)}")
            logger.exception("Error crítico")
            st.exception(e)
            return

        # =========================
        # VERIFICAR RESULTADO
        # =========================
        if resultado is None:
            st.error("No se pudo generar contenido. Intenta de nuevo.")
            return

        if resultado.get("error"):
            st.error(f"❌ {resultado['error']}")
            return

        # =========================
        # ESTRATEGIA CON BADGES
        # =========================
        decision = resultado.get("decision_router")
        if decision:
            st.markdown("##### 🧠 Estrategia")
            
            red_social = str(getattr(decision, 'red_social', 'instagram')).lower()
            
            # Mostrar badge de red social
            badge_class = {
                "instagram": "instagram-badge",
                "linkedin": "linkedin-badge", 
                "tiktok": "tiktok-badge",
                "facebook": "facebook-badge"
            }.get(red_social, "instagram-badge")
            
            badge_text = {
                "instagram": "📸 INSTAGRAM",
                "linkedin": "💼 LINKEDIN",
                "tiktok": "🎵 TIKTOK",
                "facebook": "👍 FACEBOOK"
            }.get(red_social, "📸 INSTAGRAM")
            
            st.markdown(f"""
                <div class="social-badge {badge_class}">{badge_text}</div>
            """, unsafe_allow_html=True)
            
            # Métricas
            cols = st.columns(4)
            
            with cols[0]:
                framework = str(getattr(decision, 'framework', 'PAS'))
                st.metric("Framework", framework)
            
            with cols[1]:
                tono = str(getattr(decision, 'tono', 'profesional')).capitalize()
                st.metric("Tono", tono)
            
            with cols[2]:
                requiere = getattr(decision, 'requiere_investigacion', False)
                investigacion_valor = "✅ Sí" if requiere else "—"
                st.metric("Investigación", investigacion_valor)
            
            with cols[3]:
                st.metric("Llamadas", "2")

        # =========================
        # CONTENIDO GENERADO
        # =========================
        post = resultado.get("post_generado")
        if post:
            st.markdown("##### ✨ Contenido generado")

            # Extraer datos
            if isinstance(post, dict):
                contenido = post.get("contenido", "")
                red_social = post.get("red_social", "instagram")
            else:
                contenido = getattr(post, 'contenido', '')
                red_social = getattr(post, 'red_social', 'instagram')

            # Icono según red social (se mantiene el ícono)
            iconos = {
                "instagram": "📸",
                "linkedin": "💼",
                "tiktok": "🎵",
                "facebook": "👍"
            }
            icono = iconos.get(red_social.lower(), "📝")

            # Mostrar contenido con ícono en el título (si existe)
            st.markdown(f'<div class="generated-content">', unsafe_allow_html=True)
            
            # El contenido YA INCLUYE su propio título, solo mostramos el ícono decorativo
            st.markdown(f"<div style='font-size: 1.2rem; margin-bottom: 1rem;'>{icono}</div>", unsafe_allow_html=True)
            st.markdown(contenido)
            
            st.markdown('</div>', unsafe_allow_html=True)

            # =========================
            # BOTÓN COPIAR (VERSIÓN SaaS)
            # =========================
            st.markdown("##### 📋 Copiar contenido")

            st.components.v1.html(
                f"""
                <style>
                .copy-container {{
                    position: relative;
                    width: 100%;
                }}

                .copy-textarea {{
                    width: 100%;
                    height: 260px;
                    padding: 16px;
                    font-size: 14px;
                    border-radius: 8px;
                    border: 1px solid #E0E0E0;
                    resize: none;
                    font-family: system-ui, -apple-system, sans-serif;
                }}

                .copy-btn {{
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    background: #0066CC;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 13px;
                    font-weight: 500;
                }}

                .copy-btn:hover {{
                    background: #0052A3;
                }}
                </style>

                <div class="copy-container">
                    <textarea id="contentBox" class="copy-textarea">{contenido}</textarea>
                    <button class="copy-btn" onclick="copyText()" id="copyButton">
                        📋 Copy
                    </button>
                </div>

                <script>
                function copyText() {{
                    const textarea = document.getElementById("contentBox");
                    const button = document.getElementById("copyButton");

                    navigator.clipboard.writeText(textarea.value);

                    button.innerText = "✓ Copied";
                    button.style.background = "#16a34a";

                    setTimeout(() => {{
                        button.innerText = "📋 Copy";
                        button.style.background = "#0066CC";
                    }}, 2000);
                }}
                </script>
                """,
                height=300
            )
        # Tiempo de ejecución
        if resultado.get("tiempo_inicio"):
            tiempo = time.time() - resultado["tiempo_inicio"]
            st.caption(f"⏱️ {tiempo:.1f} segundos · 2 llamadas a Gemini")

    # =========================
    # FOOTER
    # =========================
    st.markdown("""
        <div class="footer">
            ⚡ Multi-Red v2.0 · LangGraph · Gemini Pro · Tavily · Instagram · LinkedIn · TikTok · Facebook
        </div>
    """, unsafe_allow_html=True)