"""
MedTrack - MVP de Prontuário Médico Inteligente

Este aplicativo permite que um usuário:
1. Envie exames médicos (imagem)
2. Extraia o texto do exame usando OCR
3. Utilize IA para interpretar o exame
4. Armazene os resultados em um banco de dados
5. Visualize uma timeline de saúde

Tecnologias utilizadas:
- Streamlit: Interface web
- Tesseract OCR: Extração de texto de imagens
- Groq + LLM: Interpretação dos exames
- SQLite: Armazenamento do histórico
"""

# Biblioteca para criar interfaces web simples
import streamlit as st

# Biblioteca para operações de sistema (pastas, caminhos etc.)
import os

# Biblioteca OCR para leitura de texto em imagens
import pytesseract

# Biblioteca para manipulação de imagens
from PIL import Image

# Cliente da API da Groq para acesso a modelos de IA
from groq import Groq

# Biblioteca para carregar variáveis de ambiente
from dotenv import load_dotenv

# Banco de dados local
import sqlite3


# ----------------------------------------------------------
# CONFIGURAÇÃO INICIAL
# ----------------------------------------------------------

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa cliente da API Groq usando chave do ambiente
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Define caminho do executável do Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Guilherme\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


# ----------------------------------------------------------
# CONFIGURAÇÃO DO BANCO DE DADOS
# ----------------------------------------------------------

# Conecta ao banco SQLite
conn = sqlite3.connect("exames.db", check_same_thread=False)

# Cria cursor para executar comandos SQL
cursor = conn.cursor()

# Cria tabela de exames caso ainda não exista
cursor.execute("""
CREATE TABLE IF NOT EXISTS exames (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    arquivo TEXT,
    texto TEXT,
    resumo TEXT,
    data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

# Salva alterações no banco
conn.commit()


# ----------------------------------------------------------
# GARANTE QUE A PASTA DE UPLOADS EXISTA
# ----------------------------------------------------------

# Se a pasta de uploads não existir, ela será criada
if not os.path.exists("uploads"):
    os.makedirs("uploads")


# ----------------------------------------------------------
# FUNÇÃO DE ANÁLISE DE EXAMES COM IA
# ----------------------------------------------------------

def resumir_exame(texto):
    """
    Envia o texto extraído do exame para um modelo de linguagem
    hospedado na Groq para gerar uma interpretação do exame.

    Parâmetros:
        texto (str): Texto extraído do exame via OCR

    Retorna:
        str: Explicação estruturada do exame gerada pela IA
    """

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente médico que analisa exames."
            },
            {
                "role": "user",
                "content": f"""
Analise este exame médico.

Retorne:

Tipo do exame:
Principais resultados:
Pontos de atenção:
Explicação simples para paciente:

Exame:
{texto}
"""
            }
        ]
    )

    # Retorna apenas o conteúdo da resposta do modelo
    return resposta.choices[0].message.content

def buscar_historico():

    cursor.execute("""
    SELECT arquivo, resumo, data_upload
    FROM exames
    ORDER BY data_upload DESC
    """)

    exames = cursor.fetchall()

    historico = ""

    for exame in exames:

        arquivo = exame[0]
        resumo = exame[1]
        data = exame[2]

        historico += f"""
Arquivo: {arquivo}
Data: {data}
Resumo:
{resumo}

"""

    return historico

def chat_saude(pergunta):

    historico = buscar_historico()

    resposta = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Você é um assistente médico que responde perguntas sobre exames médicos."
            },
            {
                "role": "user",
                "content": f"""
Histórico médico do paciente:

{historico}

Pergunta do paciente:
{pergunta}

Responda de forma clara e simples.
"""
            }
        ]
    )

    return resposta.choices[0].message.content

def excluir_exame(nome_arquivo):

    # remove do banco
    cursor.execute(
        "DELETE FROM exames WHERE arquivo = ?",
        (nome_arquivo,)
    )

    conn.commit()

    # remove o arquivo da pasta
    caminho = os.path.join("uploads", nome_arquivo)

    if os.path.exists(caminho):
        os.remove(caminho)

# ----------------------------------------------------------
# INTERFACE DO APLICATIVO
# ----------------------------------------------------------

# Título da aplicação
st.title("Minha Saúde AI")

# Componente para upload de arquivos
arquivo = st.file_uploader("Envie seu exame")


# ----------------------------------------------------------
# PROCESSAMENTO DO EXAME ENVIADO
# ----------------------------------------------------------

if arquivo:

    # Define caminho onde o arquivo será salvo
    caminho = os.path.join("uploads", arquivo.name)

    # Salva o arquivo enviado no diretório uploads
    with open(caminho, "wb") as f:
        f.write(arquivo.read())

    # Abre a imagem enviada
    imagem = Image.open(caminho)

    # Exibe a imagem no app
    st.image(imagem, caption="Exame enviado", use_column_width=True)

    # Extrai texto da imagem usando OCR
    texto = pytesseract.image_to_string(imagem)

    # Mostra o texto bruto extraído do exame
    st.text_area("Texto extraído", texto)

    # Envia o texto para a IA gerar um resumo
    resumo = resumir_exame(texto)

    # Salva o exame no banco de dados
    cursor.execute(
        "INSERT INTO exames (arquivo, texto, resumo) VALUES (?, ?, ?)",
        (arquivo.name, texto, resumo)
    )

    conn.commit()


# ----------------------------------------------------------
# CONSTRUÇÃO DA TIMELINE DE SAÚDE
# ----------------------------------------------------------

st.subheader("Timeline de Saúde")

# Busca todos os exames no banco ordenados pela data
cursor.execute("""
SELECT arquivo, resumo, data_upload
FROM exames
ORDER BY data_upload DESC
""")

exames = cursor.fetchall()

# Estrutura para agrupar exames por ano
timeline = {}

for exame in exames:

    arquivo = exame[0]
    resumo = exame[1]
    data = exame[2]

    # Extrai o ano da data
    ano = data[:4]

    # Cria grupo do ano se ainda não existir
    if ano not in timeline:
        timeline[ano] = []

    # Adiciona exame ao ano correspondente
    timeline[ano].append((arquivo, resumo, data))


# Exibe a timeline organizada por ano
for ano in timeline:

    st.header(ano)

    for exame in timeline[ano]:

        arquivo = exame[0]
        resumo = exame[1]
        data = exame[2]

        # Cada exame pode ser expandido para ver o resumo
    with st.expander(f"📄 {arquivo} — {data}"):

        st.write(resumo)

        if st.button(f"Excluir {arquivo}"):

            excluir_exame(arquivo)

            st.success("Exame excluído com sucesso!")

            st.rerun()


st.subheader("Chat de Saúde")

pergunta = st.text_input("Pergunte algo sobre sua saúde")

if pergunta:

    resposta = chat_saude(pergunta)

    st.write("Resposta da IA:")

    st.write(resposta)


    # ----------------------------------------------------------
    # EXIBE O RESUMO DO EXAME MAIS RECENTE
    # ----------------------------------------------------------

    st.subheader("Resumo da IA")

    st.write(resumo)
