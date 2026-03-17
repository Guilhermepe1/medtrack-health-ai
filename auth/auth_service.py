import streamlit as st
import bcrypt
import re

from repositories.usuario_repository import (
    criar_usuario,
    buscar_usuario_por_username,
    buscar_usuario_por_google_id,
    buscar_usuario_por_email,
    criar_usuario_google
)
from auth.google_auth_service import (
    gerar_url_login,
    trocar_codigo_por_token,
    buscar_dados_usuario
)
from repositories.lgpd_repository import registrar_log


def registrar_usuario(nome, username, senha):

    usuario_existente = buscar_usuario_por_username(username)

    if usuario_existente:
        return False, "Usuário já existe"

    senha_hash = bcrypt.hashpw(
        senha.encode(),
        bcrypt.gensalt()
    ).decode()

    criar_usuario(nome, username, senha_hash)

    return True, "Usuário criado com sucesso"


def login(username, senha):

    usuario = buscar_usuario_por_username(username)

    if usuario is None:
        return False

    if not usuario["senha"]:
        return False

    if bcrypt.checkpw(senha.encode(), usuario["senha"].encode()):

        st.session_state["usuario_id"]   = usuario["id"]
        st.session_state["usuario_nome"] = usuario["nome"]
        st.session_state["logado"]       = True

        registrar_log(usuario["id"], "login", "Login via usuário e senha")

        return True

    return False


def iniciar_login_google():
    return gerar_url_login()


def _gerar_username_do_email(email):
    base = email.split("@")[0]
    base = re.sub(r"[^a-zA-Z0-9_]", "", base)[:20]

    username  = base
    contador  = 1

    while buscar_usuario_por_username(username):
        username = f"{base}{contador}"
        contador += 1

    return username


def finalizar_login_google(code):
    try:
        token = trocar_codigo_por_token(code)
        dados = buscar_dados_usuario(token)

        google_id  = dados.get("sub")
        email      = dados.get("email")
        nome       = dados.get("name") or email.split("@")[0]
        avatar_url = dados.get("picture")

        usuario = buscar_usuario_por_google_id(google_id)

        if not usuario:
            usuario = buscar_usuario_por_email(email)

        if not usuario:
            username   = _gerar_username_do_email(email)
            usuario_id = criar_usuario_google(
                nome, username, email, google_id, avatar_url
            )
        else:
            usuario_id = usuario["id"]
            nome       = usuario["nome"]

        st.session_state["usuario_id"]   = usuario_id
        st.session_state["usuario_nome"] = nome
        st.session_state["logado"]       = True

        registrar_log(usuario_id, "login", "Login via Google OAuth")

        return True, None

    except Exception as e:
        return False, str(e)