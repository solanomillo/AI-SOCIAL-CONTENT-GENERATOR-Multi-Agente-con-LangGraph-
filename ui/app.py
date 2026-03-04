"""
Interfaz principal con Streamlit.
Versión mínima para validar estructura.
"""

import streamlit as st


def run_app():
    st.set_page_config(
        page_title="AI Social Content Generator",
        page_icon="🚀",
        layout="centered"
    )

    st.title("🚀 AI Social Content Generator")
    st.markdown("### Generador Multi-Agente para Redes Sociales")

    st.divider()

    user_input = st.text_area(
        "Describe el contenido que quieres generar:",
        height=150
    )

    if st.button("Generar contenido"):
        if user_input.strip() == "":
            st.warning("Por favor escribe una descripción.")
        else:
            st.success("Estructura base funcionando ✅")
            st.write("En la Fase 2 conectaremos LangGraph.")