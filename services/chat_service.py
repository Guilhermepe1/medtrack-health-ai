"""
Service responsável pelo chat de saúde baseado no histórico de exames.
"""

import streamlit as st

from services.ai_service import client
from rag.vector_store import buscar_exames_semelhantes
from repositories.exame_repository import buscar_exame_por_id
from repositories.perfil_repository import perfil_para_contexto


def perguntar_saude(pergunta):

    usuario_id = st.session_state["usuario_id"]

    # busca exames semanticamente relevantes
    ids_relevantes = buscar_exames_semelhantes(usuario_id, pergunta, k=3)

    exames = []
    for exame_id in ids_relevantes:
        exame = buscar_exame_por_id(exame_id)
        if exame:
            exames.append(exame)

    contexto_exames = montar_contexto_exames(exames)

    # perfil de saúde do usuário como contexto adicional
    contexto_perfil = perfil_para_contexto(usuario_id)

    system_prompt = f"""
Você é um assistente médico que ajuda o paciente a entender seus exames.
Explique os resultados de forma clara, empática e acessível.
Nunca substitua uma consulta médica — sempre recomende buscar um profissional para decisões clínicas.

{contexto_perfil}
""".strip()

    user_prompt = f"""
Exames relevantes do paciente:

{contexto_exames}

Pergunta:
{pergunta}
""".strip()

    # histórico da conversa para contexto multi-turno
    historico = st.session_state.get("historico_chat", [])

    messages = [{"role": "system", "content": system_prompt}]

    for msg in historico[:-1]:  # exclui a última (é a pergunta atual)
        messages.append({"role": msg["role"], "content": msg["content"]})

    messages.append({"role": "user", "content": user_prompt})

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=1000
    )

    return resposta.choices[0].message.content


def montar_contexto_exames(exames):

    if not exames:
        return "Nenhum exame relevante encontrado para esta pergunta."

    contexto = ""
    for exame in exames:
        nome = getattr(exame, "nome_exame", None) or exame.arquivo
        data = getattr(exame, "data_exame", None) or exame.data_upload[:10]

        contexto += f"""
Exame: {nome}
Data: {data}

Resumo:
{exame.resumo}

"""
    return contexto