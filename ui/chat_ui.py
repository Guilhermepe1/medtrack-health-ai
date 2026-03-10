"""
UI responsável pelo chat de saúde.
"""

import streamlit as st

from services.chat_service import perguntar_saude


def render_chat():

    st.subheader("Chat de Saúde")

    pergunta = st.text_input("Pergunte algo sobre sua saúde")

    if pergunta:

        resposta = perguntar_saude(pergunta)

        st.write("Resposta da IA:")

        st.write(resposta)
