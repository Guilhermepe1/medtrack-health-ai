"""
Utilitários para manipulação de arquivos.
"""

import os

UPLOAD_FOLDER = "uploads"


def garantir_pasta_upload():
    """
    Garante que a pasta de uploads exista.
    """

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)


def salvar_arquivo_upload(arquivo):
    """
    Salva o arquivo enviado pelo usuário na pasta uploads.
    """

    garantir_pasta_upload()

    caminho = os.path.join(UPLOAD_FOLDER, arquivo.name)

    with open(caminho, "wb") as f:
        f.write(arquivo.read())

    return caminho


def remover_arquivo(nome_arquivo):
    """
    Remove um arquivo da pasta uploads.
    """

    caminho = os.path.join(UPLOAD_FOLDER, nome_arquivo)

    if os.path.exists(caminho):
        os.remove(caminho)
