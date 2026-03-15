import streamlit as st
from auth.auth_service import login
from auth.register_ui import render_registro


def render_login():

    opcao = st.radio(
        "Escolha uma opção",
        ["Login", "Registrar"]
    )

    if opcao == "Registrar":
        render_registro()
        return

    st.title("Login")

    username = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):

        sucesso = login(username, senha)

        if sucesso:
            st.success("Login realizado")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")
