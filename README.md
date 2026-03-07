# ⚡ AI Social Content Generator Multi-Agent

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-1C3C3C?style=flat&logo=langchain&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Google%20Gemini-8E75B2?style=flat&logo=googlegemini&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Tavily](https://img.shields.io/badge/Tavily-4285F4?style=flat&logo=google&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

**AI Social Content Generator** es una solución avanzada de generación de contenido para redes sociales que utiliza una arquitectura de **multi-agentes inteligentes** para crear posts optimizados para Instagram, LinkedIn, TikTok y Facebook.

---

## 📌 Descripción

A diferencia de los generadores tradicionales, este sistema orquesta múltiples agentes especializados (basados en Google Gemini 2.5 Flash) que trabajan en conjunto para:

* Analizar la idea del usuario
* Investigar tendencias relevantes (opcional con Tavily)
* Elegir la mejor red social para cada contenido
* Generar posts optimizados con el tono y formato adecuado
* Incluir hashtags estratégicos y llamados a la acción

Desarrollado con una arquitectura limpia, desacoplada y modular, el proyecto está preparado para:

* Uso personal y profesional
* Escalamiento a nuevas redes sociales
* Evolución futura a modelo SaaS

## 🚀 Stack Tecnológico

El proyecto se apoya en herramientas modernas orientadas a arquitectura escalable:

🔹 **Core IA**
* `langgraph` - Orquestación basada en grafos
* `google-generativeai` - Google Gemini 2.5 Flash
* `tavily-python` - Búsqueda de tendencias en internet

🔹 **Interfaz de Usuario**
* `streamlit` - UI profesional y responsiva

🔹 **Modelado y Validación**
* `pydantic` - Modelado estructurado de datos
* `python-dotenv` - Gestión segura de variables

🔹 **Utilidades**
* `pyperclip` - Soporte para portapapeles
* `asyncio` - Ejecución asíncrona eficiente

---

## 🧠 Arquitectura de Multi-Agentes

El núcleo del sistema se basa en la colaboración de agentes especializados, coordinados mediante un grafo de ejecución:

### 🎯 Unified Agent

Agente principal que coordina todo el flujo en **solo 2 llamadas a Gemini**:

1. **Genera contenido base** (título, cuerpo, CTA, keywords)
2. **Router Agent** decide la mejor red social
3. **Tool específica** formatea para la red elegida

### 🧭 Router Agent

Analiza el contenido y decide la red social más adecuada basándose en:
* Menciones explícitas del usuario ("para LinkedIn", "en Instagram")
* Palabras clave del contenido (profesional → LinkedIn, visual → Instagram)
* Tipo de mensaje (viral → TikTok, comunidad → Facebook)

### 🛠️ Tools por Red Social

| Tool | Red Social | Características |
|------|------------|-----------------|
| `instagram_tool.py` | 📸 Instagram | Tono visual, emojis, 5-8 hashtags, CTA en comentarios |
| `linkedin_tool.py` | 💼 LinkedIn | Tono profesional, párrafos cortos, 3-6 hashtags |
| `tiktok_tool.py` | 🎵 TikTok | Formato viral, texto corto, hashtags de tendencia |
| `facebook_tool.py` | 👍 Facebook | Estilo conversacional, ideal para comunidades |

---

## ⚙️ Funcionalidades

✅ **Generación en 2 llamadas** - Optimizado para cuotas gratuitas (5 posts/minuto)  
✅ **4 redes sociales** - Instagram, LinkedIn, TikTok y Facebook  
✅ **Detección inteligente** - El usuario puede especificar la red o la IA decide  
✅ **Investigación opcional** - Búsqueda de tendencias con Tavily  
✅ **Formato optimizado** - Cada red tiene su propio estilo  
✅ **Hashtags automáticos** - Generados a partir de keywords  
✅ **Interfaz profesional** - Badges de colores, métricas claras  
✅ **Copia simple** - Área de texto seleccionable (Ctrl+A, Ctrl+C)  
✅ **Manejo de cuota** - Verificación antes de ejecutar  
✅ **Código modular** - Fácil de extender a nuevas redes  

## 📂 Estructura del Proyecto

```text
AI-SOCIAL-CONTENT-GENERATOR/
├── agents/                 # Cerebro del sistema (Multi-Agentes)
│   ├── tools/              # Formateadores por red social
│   │   ├── instagram_tool.py
│   │   ├── linkedin_tool.py
│   │   ├── tiktok_tool.py
│   │   └── facebook_tool.py
│   ├── __init__.py
│   ├── router_agent.py     # Decide qué red social usar
│   └── unified_agent.py    # Agente principal (2 llamadas)
├── application/            # Lógica de orquestación
│   └── graph_builder.py    # Construcción del grafo (LangGraph)
├── domain/                 # Reglas de negocio y modelos
│   ├── models.py           # Estructuras de datos (Pydantic)
│   └── state.py            # Definición del estado del flujo
├── infrastructure/         # Servicios externos y clientes
│   ├── gemini_client.py    # Cliente para Google Gemini API
│   ├── tavily_client.py    # Cliente para Tavily Search
│   └── token_manager.py    # Control de tokens y límites
├── ui/                      # Interfaz de Usuario
│   └── app.py              # UI principal (Streamlit)
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
└── .env                    # Configuración (NO versionado)
```

---

## 🛠️ Instalación y Configuración

1️⃣ Clonar el repositorio
```bash
git clone https://github.com/solanomillo/AI-SOCIAL-CONTENT-GENERATOR-Multi-Agente-con-LangGraph-.git
cd AI-SOCIAL-CONTENT-GENERATOR
```

2️⃣ Crear entorno virtual
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3️⃣ Instalar dependencias
```bash
pip install -r requirements.txt
```

4️⃣ Configurar variables de entorno

Crear un archivo .env en la raíz:

```env
GEMINI_API_KEY=tu_api_key_de_gemini
TAVILY_API_KEY=tu_api_key_de_tavily  # Opcional, para investigación
GEMINI_MODEL=gemini-1.5-flash
```
⚠️ IMPORTANTE: El archivo .env no debe subirse al repositorio (está en .gitignore)

5️⃣ Ejecutar en modo desarrollo
```bash
python main.py
```
La aplicación se abrirá automáticamente en tu navegador en http://localhost:8501

---

## 🎯 Ejemplos de Uso

| Idea del usuario | Red que elegirá |
|------------------|-----------------|
| "Curso de Python para principiantes **para LinkedIn**" | ✅ LinkedIn |
| "Nuevo look de verano con mi marca de ropa" | ✅ Instagram |
| "Baile viral para promocionar mi canción" | ✅ TikTok |
| "Evento familiar este fin de semana" | ✅ Facebook |
| "Consejos para mejorar tu currículum" | ✅ LinkedIn |
| "Review de mi nuevo producto de maquillaje" | ✅ Instagram |
| "Challenge divertido con amigos" | ✅ TikTok |

---

## 🔐 Seguridad

✔️ **Sin credenciales hardcodeadas** - Todo vía variables de entorno  
✔️ **API Keys seguras** - Gemini y Tavily en `.env`  
✔️ **Arquitectura desacoplada** - Fácil de auditar  
✔️ **Preparado para producción** - Manejo de errores robusto  
✔️ **Cuota controlada** - Verificación antes de cada ejecución  

## 🏗️ Roadmap Futuro

* 🔗 **Más redes sociales** - Pinterest, Twitter/X, Threads
* 🌐 **Versión web** - SaaS multi-tenant
* 📊 **Analíticas** - Rendimiento de posts generados
* 💾 **Historial** - Guardar posts generados
* 🖼️ **Generación de imágenes** - Con IA para acompañar posts
* 📱 **App móvil** - Flutter o React Native
* 🤖 **Más agentes** - Especializados por industria

---

👨‍💻 Autor
**Julio Solano**  
🔗 GitHub: [https://github.com/solanomillo](https://github.com/solanomillo)  
📧 Email: [solanomillo144@gmail.com](mailto:solanomillo144@gmail.com)

📄 Licencia
Este proyecto está bajo la licencia MIT.
Podés usarlo, modificarlo y compartirlo libremente.
