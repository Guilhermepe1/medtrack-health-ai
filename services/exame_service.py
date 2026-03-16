"""
Service responsável pelo fluxo de processamento de exames.
"""

import streamlit as st

from services.ai_service import resumir_exame
from services.extracao_service import extrair_valores
from services.storage_service import upload_arquivo
from repositories.exame_repository import salvar_exame, buscar_exame_por_nome
from repositories.valores_repository import salvar_valores
from repositories.alertas_repository import salvar_alertas
from rag.vector_store import adicionar_exame
from services.document_reader import extrair_texto_documento
from services.exame_classifier import classificar_exame


def processar_exame(arquivo, usuario_id):
    """
    Fluxo completo de processamento de um exame:

    1. Lê conteúdo do arquivo
    2. Extrai texto (OCR)
    3. Gera resumo com IA
    4. Classifica categoria
    5. Faz upload para Supabase Storage
    6. Salva metadados no banco
    7. Extrai valores estruturados
    8. Gera alertas clínicos para valores fora da referência
    9. Indexa embedding no pgvector
    """

    conteudo = arquivo.read()

    texto = extrair_texto_documento(arquivo)
    resumo = resumir_exame(texto)
    categoria = classificar_exame(texto)

    storage_path = upload_arquivo(usuario_id, arquivo.name, conteudo)

    if not storage_path:
        st.error("Erro ao salvar arquivo no storage. Tente novamente.")
        return None, texto, resumo, categoria

    salvar_exame(usuario_id, arquivo.name, texto, resumo, categoria, storage_path)

    exame = buscar_exame_por_nome(usuario_id, arquivo.name)

    if exame:
        resultado = extrair_valores(texto)
        valores = resultado.get("valores", [])
        data_coleta = resultado.get("data_coleta")

        salvar_valores(
            exame_id=exame.id,
            usuario_id=usuario_id,
            data_coleta=data_coleta,
            valores=valores
        )

        salvar_alertas(
            usuario_id=usuario_id,
            exame_id=exame.id,
            valores=valores
        )

        adicionar_exame(usuario_id, exame.id, texto)

    return storage_path, texto, resumo, categoria