import streamlit as st
from auth.auth_service import registrar_usuario


def render_registro():

    st.title("Criar conta")

    nome = st.text_input("Nome")
    username = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    confirmar = st.text_input("Confirmar senha", type="password")

    if st.button("Registrar"):

        if senha != confirmar:
            st.error("As senhas não coincidem")
            return

        sucesso, mensagem = registrar_usuario(nome, username, senha)

        if sucesso:
            st.success(mensagem)
        else:
            st.error(mensagem)
