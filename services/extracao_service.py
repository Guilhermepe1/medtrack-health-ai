"""
Service responsável por extrair valores estruturados de exames laboratoriais.
"""

import json
import streamlit as st
from groq import Groq
import numpy as np

client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

PROMPT_EXTRACAO = """
Você é um especialista em laudos laboratoriais.
Analise o texto do exame e extraia os valores dos parâmetros laboratoriais.

Retorne APENAS um JSON válido, sem texto adicional, no seguinte formato:
{
  "data_coleta": "YYYY-MM-DD ou null se não encontrar",
  "valores": [
    {
      "parametro": "nome do parâmetro",
      "valor": número ou null,
      "unidade": "unidade de medida",
      "referencia_min": número ou null,
      "referencia_max": número ou null,
      "status": "normal", "alto" ou "baixo"
    }
  ]
}

Parâmetros comuns do hemograma para extrair:
- Hemoglobina, Hematócrito, Eritrócitos (hemácias)
- VCM, HCM, CHCM, RDW
- Leucócitos totais
- Neutrófilos, Linfócitos, Monócitos, Eosinófilos, Basófilos
- Plaquetas

Regras:
- valor deve ser sempre número (float), nunca string
- Se o parâmetro não tiver valor numérico identificável, omita-o da lista
- status deve ser "normal", "alto" ou "baixo" baseado nos valores de referência
- Se não houver referência, defina status como "normal"
"""


def extrair_valores(texto: str) -> dict:
    """
    Usa a IA para extrair valores estruturados do texto do exame.
    Retorna dicionário com data_coleta e lista de valores.
    """
    try:
        resposta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": PROMPT_EXTRACAO},
                {"role": "user", "content": f"Texto do exame:\n\n{texto}"}
            ],
            temperature=0.1
        )

        conteudo = resposta.choices[0].message.content.strip()

        # remove possíveis blocos de markdown
        if conteudo.startswith("```"):
            conteudo = conteudo.split("```")[1]
            if conteudo.startswith("json"):
                conteudo = conteudo[4:]

        return json.loads(conteudo)

    except Exception as e:
        print(f"Erro ao extrair valores: {e}")
        return {"data_coleta": None, "valores": []}
