"""
Aplicação principal do Minha Saúde AI
Responsável apenas por montar a interface.
"""

import streamlit as st

from auth.login_ui import render_login
from ui.upload_ui import render_upload
from ui.timeline_ui import render_timeline
from ui.chat_ui import render_chat
from ui.valores_ui import render_valores
from ui.alertas_ui import render_alertas, render_badge_alertas


# deve ser a primeira chamada Streamlit do script
st.set_page_config(
    page_title="Minha Saúde AI",
    page_icon="🩺",
    layout="wide"
)


def main():

    if "logado" not in st.session_state:
        render_login()
        return

    st.sidebar.write(f"Usuário: {st.session_state['usuario_nome']}")

    if st.sidebar.button("Logout"):
        st.session_state.clear()
        st.rerun()

    st.title("🩺 Minha Saúde AI")

    st.markdown(
        """
        Faça upload de seus exames médicos, acompanhe seu histórico
        e tire dúvidas sobre sua saúde com ajuda de IA.
        """
    )

    # badge de alertas não lidos — visível em todas as telas
    render_badge_alertas()

    st.divider()

    render_upload()

    st.divider()

    render_timeline()

    st.divider()

    render_valores()

    st.divider()

    render_alertas()

    st.divider()

    render_chat()


if __name__ == "__main__":
    main()