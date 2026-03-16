import streamlit as st
from auth.auth_service import login, iniciar_login_google, finalizar_login_google
from auth.register_ui import render_registro


def render_login():

    # intercepta callback do Google (código na URL)
    params = st.query_params

    if "code" in params:
        with st.spinner("Autenticando com Google..."):
            sucesso, erro = finalizar_login_google(params["code"])

        if sucesso:
            st.query_params.clear()
            st.rerun()
        else:
            st.error(f"Erro na autenticação com Google: {erro}")
            st.query_params.clear()
        return

    # tela normal de login
    opcao = st.radio("Escolha uma opção", ["Login", "Registrar"])

    if opcao == "Registrar":
        render_registro()
        return

    st.title("Login")

    # botão Google
    url_google = iniciar_login_google()

    st.link_button(
        "🔵  Entrar com Google",
        url=url_google,
        use_container_width=True
    )

    st.divider()

    # login tradicional
    username = st.text_input("Usuário")
    senha    = st.text_input("Senha", type="password")

    if st.button("Entrar", use_container_width=True):

        sucesso = login(username, senha)

        if sucesso:
            st.success("Login realizado")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")