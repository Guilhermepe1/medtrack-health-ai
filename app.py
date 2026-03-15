"""
Aplicação principal do Minha Saúde AI
Responsável apenas por montar a interface.
"""

import streamlit as st

from ui.upload_ui import render_upload
from ui.timeline_ui import render_timeline
from ui.chat_ui import render_chat
from auth.login_ui import render_login


def main():

    if "logado" not in st.session_state:

        render_login()
        return

    st.sidebar.write(f"Usuário: {st.session_state['usuario_nome']}")

    if st.sidebar.button("Logout"):

        st.session_state.clear()
        st.rerun()

    st.set_page_config(
        page_title="Minha Saúde AI",
        page_icon="🩺",
        layout="wide"
    )

    st.title("🩺 Minha Saúde AI")

    st.markdown(
        """
        Faça upload de seus exames médicos, acompanhe seu histórico
        e tire dúvidas sobre sua saúde com ajuda de IA.
        """
    )

    st.divider()

    render_upload()

    st.divider()

    render_timeline()

    st.divider()

    render_chat()


if __name__ == "__main__":
    main()
