# Service responsável pela autenticação OAuth com Google.


import streamlit as st
from authlib.integrations.requests_client import OAuth2Session


GOOGLE_AUTH_URL     = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL    = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
SCOPE               = "openid email profile"


def get_oauth_session():
    return OAuth2Session(
        client_id=st.secrets["GOOGLE_CLIENT_ID"],
        client_secret=st.secrets["GOOGLE_CLIENT_SECRET"],
        redirect_uri=st.secrets["GOOGLE_REDIRECT_URI"],
        scope=SCOPE
    )


def gerar_url_login():
    """
    Gera a URL de redirecionamento para o Google.
    Salva o state na sessão para validação posterior.
    """
    session = get_oauth_session()

    url, state = session.create_authorization_url(
        GOOGLE_AUTH_URL,
        access_type="offline",
        prompt="select_account"
    )

    st.session_state["oauth_state"] = state

    return url


def trocar_codigo_por_token(code):
    """
    Troca o código de autorização pelo token de acesso.
    """
    session = get_oauth_session()

    token = session.fetch_token(
        GOOGLE_TOKEN_URL,
        code=code
    )

    return token


def buscar_dados_usuario(token):
    """
    Busca os dados do usuário autenticado no Google.
    Retorna dict com: email, name, sub (google_id)
    """
    session = get_oauth_session()
    session.token = token

    resp = session.get(GOOGLE_USERINFO_URL)
    resp.raise_for_status()

    return resp.json()