import streamlit as st
import bcrypt

from repositories.usuario_repository import criar_usuario, buscar_usuario_por_username


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

    senha_hash = usuario[3]

    if bcrypt.checkpw(senha.encode(), senha_hash.encode()):

        st.session_state["usuario_id"] = usuario[0]
        st.session_state["usuario_nome"] = usuario[1]
        st.session_state["logado"] = True

        return True

    return False
