"""
Service responsável pelo fluxo de processamento de exames.
"""

import os

from services.ai_service import resumir_exame
from repositories.exame_repository import salvar_exame
from rag.vector_store import adicionar_exame
from repositories.exame_repository import salvar_exame, buscar_exame_por_nome
from services.document_reader import extrair_texto_documento
from services.exame_classifier import classificar_exame


UPLOAD_FOLDER = "uploads"


def processar_exame(arquivo, usuario_id):
    """
    Fluxo completo de processamento de um exame:

    1. Salva arquivo
    2. Extrai texto (OCR)
    3. Gera resumo com IA
    4. Salva no banco
    """

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    caminho = os.path.join(UPLOAD_FOLDER, arquivo.name)

    with open(caminho, "wb") as f:
        f.write(arquivo.read())

    texto = extrair_texto_documento(arquivo)

    resumo = resumir_exame(texto)

    categoria = classificar_exame(texto)

    salvar_exame(usuario_id, arquivo.name, texto, resumo, categoria)
    
    exame = buscar_exame_por_nome(usuario_id, arquivo.name)

    adicionar_exame(usuario_id, resumo)

    return caminho, texto, resumo, categoria
