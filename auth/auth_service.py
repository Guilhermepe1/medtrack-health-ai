import streamlit as st
import bcrypt

from repositories.usuario_repository import buscar_usuario_por_username


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
