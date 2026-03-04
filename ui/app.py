"""
Interfaz principal con Streamlit.
Ahora ejecuta flujo completo con branching.
"""

import streamlit as st
from application.graph_builder import construir_grafo


def run_app():
    st.set_page_config(
        page_title="AI Social Content Generator",
        page_icon="🚀",
        layout="centered"
    )

    st.title("🚀 AI Social Content Generator")
    st.markdown("### Generador Multi-Agente con LangGraph")

    st.divider()

    user_input = st.text_area(
        "Describe el contenido que quieres generar:",
        height=150
    )

    if st.button("Generar contenido"):
        if not user_input.strip():
            st.warning("Por favor escribe una descripción.")
            return

        grafo = construir_grafo()

        estado_inicial = {
            "prompt_usuario": user_input,
            "tipo_contenido": None,
            "red_social": None,
            "framework": None,
            "tono": None,
            "requiere_investigacion": None,
            "resultado": None,
        }

        resultado = grafo.invoke(estado_inicial)

        if resultado.get("resultado"):
            st.success("Contenido generado:")
            st.write(resultado["resultado"])
        else:
            st.error("No se generó contenido. Revisa la decisión del router.")
            st.json(resultado)