import os
import faiss
import numpy as np

from services.embedding_service import gerar_embedding

RAG_FOLDER = "rag"

# dimensão do embedding (ajuste conforme seu modelo)
DIMENSION = 384


def _get_index_path(usuario_id):
    """
    Retorna o caminho do índice do usuário.
    """
    return os.path.join(RAG_FOLDER, f"user_{usuario_id}.index")


def carregar_index(usuario_id):
    """
    Carrega o índice FAISS do usuário ou cria um novo.
    """

    caminho = _get_index_path(usuario_id)

    if os.path.exists(caminho):
        return faiss.read_index(caminho)

    return faiss.IndexFlatL2(DIMENSION)


def salvar_index(usuario_id, index):

    caminho = _get_index_path(usuario_id)

    faiss.write_index(index, caminho)


def adicionar_exame(usuario_id, texto):

    index = carregar_index(usuario_id)

    embedding = gerar_embedding(texto)

    vetor = np.array([embedding]).astype("float32")

    index.add(vetor)

    salvar_index(usuario_id, index)


def buscar_exames_semelhantes(usuario_id, pergunta, k=3):

    index = carregar_index(usuario_id)

    if index.ntotal == 0:
        return []

    embedding = gerar_embedding(pergunta)

    vetor = np.array([embedding]).astype("float32")

    distancias, indices = index.search(vetor, k)

    return indices[0]
