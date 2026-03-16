"""
UI responsável pelo upload de exames.
IA extrai os metadados e o usuário confirma/corrige antes de salvar.
"""

import streamlit as st
import os
from PIL import Image
import io
from datetime import date

from services.exame_service import processar_exame
from services.extracao_service import extrair_metadados_e_valores
from services.document_reader import extrair_texto_documento


def _parse_data(data_str):
    """Tenta converter string YYYY-MM-DD para date, retorna None se falhar."""
    if not data_str:
        return None
    try:
        partes = data_str.split("-")
        return date(int(partes[0]), int(partes[1]), int(partes[2]))
    except Exception:
        return None


def render_upload():

    usuario_id = st.session_state["usuario_id"]

    arquivo = st.file_uploader(
        "Enviar exame",
        type=["png", "jpg", "jpeg", "pdf"]
    )

    if not arquivo:
        return

    # guarda conteúdo em memória antes de consumir o buffer
    conteudo = arquivo.read()
    arquivo.seek(0)

    # preview do arquivo
    ext = os.path.splitext(arquivo.name)[1].lower()

    if ext in [".png", ".jpg", ".jpeg"]:
        imagem = Image.open(io.BytesIO(conteudo))
        st.image(imagem, caption="Exame enviado", use_container_width=True)
    else:
        st.info("📄 PDF recebido com sucesso.")
        st.download_button(
            label="Baixar PDF",
            data=conteudo,
            file_name=arquivo.name,
            mime="application/pdf"
        )

    st.divider()

    # extrai metadados via IA
    with st.spinner("🤖 Analisando documento..."):
        texto = extrair_texto_documento(arquivo)
        resultado = extrair_metadados_e_valores(texto)

    st.markdown("#### Confirme os dados do exame")
    st.caption("A IA preencheu automaticamente. Corrija se necessário antes de salvar.")

    col1, col2 = st.columns(2)

    with col1:
        nome_exame = st.text_input(
            "Nome do exame",
            value=resultado.get("nome_exame") or "",
            placeholder="Ex: Hemograma Completo"
        )
        medico = st.text_input(
            "Médico solicitante",
            value=resultado.get("medico") or "",
            placeholder="Ex: Dr. João Silva"
        )

    with col2:
        data_exame = st.date_input(
            "Data do exame",
            value=_parse_data(resultado.get("data_exame")),
            format="DD/MM/YYYY"
        )
        hospital = st.text_input(
            "Hospital / Laboratório",
            value=resultado.get("hospital") or "",
            placeholder="Ex: Laboratório Fleury"
        )

    if st.button("💾 Salvar exame", use_container_width=True):
        with st.spinner("Salvando e indexando..."):
            arquivo.seek(0)
            storage_path, _, resumo, categoria = processar_exame(
                arquivo=arquivo,
                usuario_id=usuario_id,
                nome_exame=nome_exame or None,
                data_exame=str(data_exame) if data_exame else None,
                medico=medico or None,
                hospital=hospital or None,
                conteudo=conteudo,
                texto=texto,
            )

        if storage_path:
            st.success(f"✅ Exame salvo! Categoria: **{categoria}**")

            with st.expander("Ver resumo da IA"):
                st.write(resumo)

            with st.expander("Ver texto extraído"):
                st.text_area("", texto, height=200, label_visibility="collapsed")
        else:
            st.error("Erro ao salvar o exame. Tente novamente.")