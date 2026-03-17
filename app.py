"""
Aplicação principal do MedTrack Health AI.
"""

import streamlit as st
from datetime import datetime

from auth.login_ui import render_login
from ui.upload_ui import render_upload
from ui.timeline_ui import render_timeline
from ui.chat_ui import render_chat
from ui.valores_ui import render_valores
from ui.alertas_ui import render_alertas
from ui.perfil_ui import render_avatar_sidebar, render_modal_perfil
from repositories.alertas_repository import buscar_alertas_nao_lidos
from theme import aplicar_tema, sidebar_logo, page_header

st.set_page_config(
    page_title="MedTrack Health AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


def get_saudacao():
    hora = datetime.now().hour
    if hora < 12:
        return "Bom dia"
    elif hora < 18:
        return "Boa tarde"
    return "Boa noite"


def render_sidebar():
    sidebar_logo()

    # avatar com botão de perfil
    render_avatar_sidebar(st.session_state["usuario_nome"])

    nao_lidos    = buscar_alertas_nao_lidos(st.session_state["usuario_id"])
    alerta_badge = f" 🔴 {len(nao_lidos)}" if nao_lidos else ""

    paginas = {
        "upload":   ("📤", "Enviar Exame"),
        "timeline": ("🗂️", "Meus Exames"),
        "valores":  ("📊", "Valores Laboratoriais"),
        "alertas":  ("⚠️", f"Alertas{alerta_badge}"),
        "chat":     ("💬", "Chat de Saúde"),
    }

    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "upload"

    st.sidebar.markdown(
        '<div class="nav-label">Menu</div>',
        unsafe_allow_html=True
    )

    for key, (icone, label) in paginas.items():
        ativo = st.session_state["pagina"] == key
        if st.sidebar.button(
            f"{icone}  {label}",
            key=f"nav_{key}",
            use_container_width=True,
            type="primary" if ativo else "secondary"
        ):
            st.session_state["pagina"] = key
            st.session_state["modal_perfil"] = False
            st.rerun()

    st.sidebar.divider()

    if st.sidebar.button("🚪  Sair", use_container_width=True, type="secondary"):
        st.session_state.clear()
        st.rerun()


def main():

    aplicar_tema()

    if "logado" not in st.session_state:
        render_login()
        return

    render_sidebar()

    # modal de perfil — renderiza por cima do conteúdo atual
    if st.session_state.get("modal_perfil"):
        render_modal_perfil()
        return

    pagina   = st.session_state.get("pagina", "upload")
    nome     = st.session_state["usuario_nome"]
    saudacao = get_saudacao()

    if pagina == "upload":
        page_header(
            f"{saudacao}, {nome} 👋",
            "Envie um novo exame para análise automática"
        )
        render_upload()

    elif pagina == "timeline":
        page_header("Meus Exames", "Histórico completo dos seus exames")
        render_timeline()

    elif pagina == "valores":
        page_header("Valores Laboratoriais", "Acompanhe a evolução dos seus indicadores")
        render_valores()

    elif pagina == "alertas":
        page_header("Alertas Clínicos", "Valores que merecem atenção")
        render_alertas()

    elif pagina == "chat":
        page_header("Chat de Saúde", "Tire dúvidas sobre seus exames com IA")
        render_chat()


if __name__ == "__main__":
    main()