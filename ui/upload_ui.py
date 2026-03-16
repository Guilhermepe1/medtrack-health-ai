"""
UI responsável pelo upload de exames.
"""

import streamlit as st
import os
from PIL import Image
import io

from services.exame_service import processar_exame


def render_upload():

    st.subheader("Upload de Exame")

    usuario_id = st.session_state["usuario_id"]

    arquivo = st.file_uploader(
        "Enviar exame",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if arquivo:

        # guarda o conteúdo em memória antes do processar_exame consumir o buffer
        conteudo = arquivo.read()
        arquivo.seek(0)

        storage_path, texto, resumo, categoria = processar_exame(arquivo, usuario_id)

        st.success(f"Tipo de exame detectado: {categoria}")

        ext = os.path.splitext(arquivo.name)[1].lower()

        # se for imagem — usa o conteúdo em memória
        if ext in [".png", ".jpg", ".jpeg"]:
            imagem = Image.open(io.BytesIO(conteudo))
            st.image(imagem, caption="Exame enviado", use_container_width=True)

        # se for PDF — botão de download direto do buffer
        elif ext == ".pdf":
            st.info("PDF enviado com sucesso.")
            st.download_button(
                label="Abrir / Baixar PDF",
                data=conteudo,
                file_name=arquivo.name,
                mime="application/pdf"
            )

        st.text_area("Texto extraído", texto, height=200)

        st.subheader("Resumo da IA")
        st.write(resumo)