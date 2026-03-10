"""
UI responsável pelo upload de exames.
"""

import streamlit as st
import os
from PIL import Image

from services.exame_service import processar_exame


def render_upload():

    st.subheader("Upload de Exame")

    arquivo = st.file_uploader(
        "Enviar exame",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if arquivo:

        caminho, texto, resumo, categoria = processar_exame(arquivo)

        st.success(f"Tipo de exame detectado: {categoria}")

        # detectar extensão do arquivo salvo
        ext = os.path.splitext(caminho)[1].lower()

        # se for imagem
        if ext in [".png", ".jpg", ".jpeg"]:

            imagem = Image.open(caminho)

            st.image(
                imagem,
                caption="Exame enviado",
                use_column_width=True
            )

        # se for PDF
        elif ext == ".pdf":

            st.info("PDF enviado com sucesso.")

            with open(caminho, "rb") as f:

                st.download_button(
                    label="Abrir / Baixar PDF",
                    data=f,
                    file_name=os.path.basename(caminho),
                    mime="application/pdf"
                )

        st.text_area("Texto extraído", texto, height=200)

        st.subheader("Resumo da IA")

        st.write(resumo)


