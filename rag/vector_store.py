"""
Responsável por armazenar e buscar embeddings.
"""

import faiss
import numpy as np

from rag.embedding_service import gerar_embedding

# dimensão do modelo MiniLM
DIMENSION = 384

index = faiss.IndexFlatL2(DIMENSION)

# mapa id_exame -> posição no vetor
id_map = []


def adicionar_exame(exame_id, texto):
    embedding = gerar_embedding(texto)

    vetor = np.array([embedding]).astype("float32")

    index.add(vetor)

    id_map.append(exame_id)


def buscar_exames(pergunta, k=3):

    # se não houver nada no index ainda
    if index.ntotal == 0:
        return []

    embedding = gerar_embedding(pergunta)

    vetor = np.array([embedding]).astype("float32")

    distancias, indices = index.search(vetor, k)

    resultados = []

    # FAISS retorna matriz 2D → pegamos a primeira linha
    for i in indices[0]:

        # -1 significa que não encontrou resultado
        if i != -1 and i < len(id_map):
            resultados.append(id_map[i])

    return resultados
