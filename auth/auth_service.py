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

    if bcrypt.checkpw(senha.encode(), usuario["senha"].encode()):

        st.session_state["usuario_id"] = usuario["id"]
        st.session_state["usuario_nome"] = usuario["nome"]
        st.session_state["logado"] = True

        return True

    return False