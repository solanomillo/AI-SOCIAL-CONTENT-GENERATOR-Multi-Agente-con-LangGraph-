"""
Modelos del dominio para el sistema AI Social Content Generator.
Actualizado para soportar múltiples redes sociales.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


# =========================
# ENUMS DEL DOMINIO
# =========================


class RedSocial(str, Enum):
    """Redes sociales soportadas."""
    INSTAGRAM = "instagram"
    LINKEDIN = "linkedin"
    TIKTOK = "tiktok"
    FACEBOOK = "facebook"


class TipoContenido(str, Enum):
    """Tipo de contenido a generar."""
    PROMOCIONAL = "promocional"
    EDUCATIVO = "educativo"
    STORYTELLING = "storytelling"
    VIRAL = "viral"
    COMUNIDAD = "comunidad"


class TonoContenido(str, Enum):
    """Tono del contenido generado."""
    PROFESIONAL = "profesional"
    CERCANO = "cercano"
    DIVERTIDO = "divertido"
    PERSUASIVO = "persuasivo"
    INFORMATIVO = "informativo"
    EMOCIONAL = "emocional"


class FrameworkContenido(str, Enum):
    """Framework de copywriting."""
    AIDA = "AIDA"
    PAS = "PAS"
    STORY = "STORY"


# =========================
# MODELOS PRINCIPALES
# =========================


class DecisionRouter(BaseModel):
    """Decisión del router_agent para dirigir el flujo."""

    tipo_contenido: TipoContenido
    red_social: RedSocial  # Ahora acepta instagram, linkedin, tiktok, facebook
    framework: FrameworkContenido
    tono: TonoContenido
    requiere_investigacion: bool = False

    model_config = ConfigDict(use_enum_values=True)


# =========================
# MODELOS DE PRODUCTO
# =========================


class Producto(BaseModel):
    """Información del producto o servicio."""

    nombre: str
    descripcion: str
    caracteristicas: List[str] = Field(default_factory=list)
    beneficios: List[str] = Field(default_factory=list)


# =========================
# INVESTIGACIÓN (TAVILY)
# =========================


class ResultadoInvestigacion(BaseModel):
    """Resultado de la investigación con Tavily."""

    resumen: str = ""
    tendencias: List[str] = Field(default_factory=list)
    insights_marketing: List[str] = Field(default_factory=list)


# =========================
# CONTENIDO GENERADO
# =========================


class PostGenerado(BaseModel):
    """Post generado por el agente de red social."""

    titulo: Optional[str] = None
    contenido: str
    hashtags: List[str] = Field(default_factory=list)
    red_social: Optional[RedSocial] = None

    model_config = ConfigDict(use_enum_values=True)


class PostOptimizado(BaseModel):
    """Post refinado por el optimizer_agent."""

    contenido_mejorado: str
    hashtags_optimizados: List[str] = Field(default_factory=list)
    call_to_action: Optional[str] = None
    post_original: Optional[PostGenerado] = None


# =========================
# RESULTADO FINAL
# =========================


class ResultadoFinal(BaseModel):
    """Resultado final para la UI."""

    red_social: RedSocial
    contenido: str
    hashtags: List[str] = Field(default_factory=list)
    titulo: Optional[str] = None
    fue_optimizado: bool = False
    investigacion_utilizada: Optional[ResultadoInvestigacion] = None
    estrategia: Optional[DecisionRouter] = None

    model_config = ConfigDict(use_enum_values=True)