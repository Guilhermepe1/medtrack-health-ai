"""
UI responsável pelo chat de saúde.
"""

import streamlit as st

from services.chat_service import perguntar_saude


def render_chat():

    st.subheader("Chat de Saúde")

    # inicializa histórico na sessão
    if "historico_chat" not in st.session_state:
        st.session_state.historico_chat = []

    # exibe histórico de mensagens
    for mensagem in st.session_state.historico_chat:
        with st.chat_message(mensagem["role"]):
            st.write(mensagem["content"])

    # input do usuário
    pergunta = st.chat_input("Pergunte algo sobre sua saúde...")

    if pergunta:

        # exibe e salva pergunta do usuário
        with st.chat_message("user"):
            st.write(pergunta)

        st.session_state.historico_chat.append({
            "role": "user",
            "content": pergunta
        })

        # busca resposta da IA
        with st.chat_message("assistant"):
            with st.spinner("Consultando seus exames..."):
                resposta = perguntar_saude(pergunta)
            st.write(resposta)

        st.session_state.historico_chat.append({
            "role": "assistant",
            "content": resposta
        })