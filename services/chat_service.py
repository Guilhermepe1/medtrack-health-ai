"""
Service responsável pelo chat de saúde baseado no histórico de exames.
"""

import streamlit as st

from services.ai_service import client
from rag.vector_store import buscar_exames_semelhantes
from repositories.exame_repository import buscar_exame_por_id


def perguntar_saude(pergunta):

    # pegar usuário logado
    usuario_id = st.session_state["usuario_id"]

    # buscar exames semanticamente relevantes no RAG
    ids_relevantes = buscar_exames_semelhantes(usuario_id, pergunta, k=3)

    exames = []

    for exame_id in ids_relevantes:

        exame = buscar_exame_por_id(exame_id)

        if exame:
            exames.append(exame)

    contexto = montar_contexto_exames(exames)

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
Você é um assistente médico que ajuda o paciente a entender seus exames.
Explique os resultados de forma clara, mas sem substituir um médico.
"""
            },
            {
                "role": "user",
                "content": f"""
Exames relevantes do paciente:

{contexto}

Pergunta do paciente:
{pergunta}
"""
            }
        ]
    )

    return resposta.choices[0].message.content


def montar_contexto_exames(exames):

    contexto = ""

    for exame in exames:

        contexto += f"""
Arquivo: {exame.arquivo}
Data: {exame.data_upload}

Resumo:
{exame.resumo}

"""

    return contexto
