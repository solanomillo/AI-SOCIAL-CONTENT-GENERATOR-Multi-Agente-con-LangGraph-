"""
Modelos Pydantic para validar respuestas estructuradas del Router.
"""

from pydantic import BaseModel


class DecisionRouter(BaseModel):
    tipo_contenido: str
    red_social: str
    framework: str
    tono: str
    requiere_investigacion: bool