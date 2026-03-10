"""
Aplicação principal do Minha Saúde AI
Responsável apenas por montar a interface.
"""

import streamlit as st

from ui.upload_ui import render_upload
from ui.timeline_ui import render_timeline
from ui.chat_ui import render_chat


def main():

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
