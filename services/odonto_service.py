"""
Service responsável pelo processamento de documentos odontológicos.
Extrai informações de laudos, radiografias e planos de tratamento.
"""

import json
import streamlit as st
from groq import Groq

client = Groq(api_key=st.secrets.get("GROQ_API_KEY"))

PROMPT_ODONTO = """
Você é um especialista em documentos odontológicos.
Analise o texto extraído do documento e retorne APENAS um JSON válido.

Formato esperado:
{
  "tipo": "laudo" | "plano_tratamento" | "radiografia" | "foto",
  "subtipo": "panoramica" | "periapical" | "bite-wing" | null,
  "data_registro": "YYYY-MM-DD ou null",
  "dentista": "nome do dentista ou null",
  "clinica": "nome da clínica ou null",
  "resumo": "resumo claro em linguagem acessível para o paciente",
  "dentes_afetados": [
    {
      "numero": número FDI do dente (ex: 11, 36),
      "status": "carie" | "restaurado" | "ausente" | "implante" | "coroa" | "tratamento_canal" | "saudavel",
      "observacao": "descrição breve do achado neste dente ou null"
    }
  ],
  "tratamentos_realizados": ["lista de tratamentos já feitos"],
  "tratamentos_planejados": ["lista de tratamentos a fazer"],
  "observacoes_gerais": "outras observações relevantes ou null"
}

Numeração FDI dos dentes:
- Superior direito: 11-18 (incisivo central ao siso)
- Superior esquerdo: 21-28
- Inferior esquerdo: 31-38
- Inferior direito: 41-48

Regras:
- Se não conseguir identificar números FDI específicos, deixe dentes_afetados como []
- resumo deve ser em português, claro e sem jargão técnico excessivo
- tipo deve refletir o conteúdo real do documento
"""


def extrair_dados_odonto(texto: str) -> dict:
    """
    Usa IA para extrair dados estruturados de documento odontológico.
    """
    try:
        resposta = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": PROMPT_ODONTO},
                {"role": "user", "content": f"Documento odontológico:\n\n{texto}"}
            ],
            temperature=0.1
        )

        conteudo = resposta.choices[0].message.content.strip()

        if conteudo.startswith("```"):
            conteudo = conteudo.split("```")[1]
            if conteudo.startswith("json"):
                conteudo = conteudo[4:]

        return json.loads(conteudo)

    except Exception as e:
        print(f"Erro ao extrair dados odonto: {e}")
        return {
            "tipo": "laudo",
            "subtipo": None,
            "data_registro": None,
            "dentista": None,
            "clinica": None,
            "resumo": "Não foi possível extrair automaticamente. Revise manualmente.",
            "dentes_afetados": [],
            "tratamentos_realizados": [],
            "tratamentos_planejados": [],
            "observacoes_gerais": None
        }


def resumir_para_chat(registros) -> str:
    """
    Formata registros odontológicos como contexto para o chat de IA.
    """
    if not registros:
        return ""

    linhas = ["=== Histórico odontológico ==="]

    for r in registros:
        data = str(r.get("data_registro") or r.get("created_at", ""))[:10]
        tipo = r.get("tipo", "registro").replace("_", " ").title()
        linhas.append(f"\n{tipo} — {data}")
        if r.get("dentista"):
            linhas.append(f"Dentista: {r['dentista']}")
        if r.get("resumo"):
            linhas.append(f"Resumo: {r['resumo']}")

    linhas.append("=============================")
    return "\n".join(linhas)