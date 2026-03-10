"""
Service responsável pelo chat de saúde baseado no histórico de exames.
"""

from services.ai_service import client
from repositories.exame_repository import buscar_exames_relevantes
from rag.vector_store import buscar_exames
from repositories.exame_repository import buscar_exame_por_id


def perguntar_saude(pergunta):

    ids_relevantes = buscar_exames(pergunta, k=3)

    exames = []

    for exame_id in ids_relevantes:

        exame = buscar_exame_por_id(exame_id)

        if exame:
            exames.append(exame)

    contexto = ""

    for exame in exames:

        contexto += f"""
Arquivo: {exame.arquivo}
Data: {exame.data_upload}

Resumo:
{exame.resumo}

"""

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente médico."
            },
            {
                "role": "user",
                "content": f"""
Exames relevantes do paciente:

{contexto}

Pergunta:
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
