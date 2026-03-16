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
        return False  # usuário criado via Google, sem senha

    if bcrypt.checkpw(senha.encode(), usuario["senha"].encode()):

        st.session_state["usuario_id"]   = usuario["id"]
        st.session_state["usuario_nome"] = usuario["nome"]
        st.session_state["logado"]       = True

        return True

    return False


def iniciar_login_google():
    """
    Gera e retorna a URL de login do Google.
    """
    return gerar_url_login()


def _gerar_username_do_email(email):
    """
    Gera um username único baseado no email.
    Ex: guilherme@gmail.com → guilherme
    """
    base = email.split("@")[0]
    base = re.sub(r"[^a-zA-Z0-9_]", "", base)[:20]

    # garante unicidade adicionando sufixo se necessário
    username = base
    contador = 1

    while buscar_usuario_por_username(username):
        username = f"{base}{contador}"
        contador += 1

    return username


def finalizar_login_google(code):
    """
    Finaliza o fluxo OAuth: troca o código pelo token,
    busca os dados do usuário e cria/loga na sessão.
    """
    try:
        token = trocar_codigo_por_token(code)
        dados = buscar_dados_usuario(token)

        google_id  = dados.get("sub")
        email      = dados.get("email")
        nome       = dados.get("name") or email.split("@")[0]
        avatar_url = dados.get("picture")

        # busca por google_id primeiro
        usuario = buscar_usuario_por_google_id(google_id)

        # tenta por email se ainda não vinculado
        if not usuario:
            usuario = buscar_usuario_por_email(email)

        if not usuario:
            # primeiro acesso — cria usuário automaticamente
            username   = _gerar_username_do_email(email)
            usuario_id = criar_usuario_google(nome, username, email, google_id, avatar_url)
        else:
            usuario_id = usuario["id"]
            nome       = usuario["nome"]

        st.session_state["usuario_id"]   = usuario_id
        st.session_state["usuario_nome"] = nome
        st.session_state["logado"]       = True

        return True, None

    except Exception as e:
        return False, str(e)