"""
Repository responsável por todas as operações no banco
relacionadas à entidade Exame.
"""

import os
from database.db import conn
from models.exame import Exame

UPLOAD_FOLDER = "uploads"


def salvar_exame(arquivo, texto, resumo, categoria):
    """
    Salva um novo exame no banco de dados.
    """

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO exames (arquivo, texto, resumo, categoria)
        VALUES (?, ?, ?, ?)
        """,
        (arquivo, texto, resumo, categoria)
    )

    conn.commit()


def listar_exames():

    cursor = conn.cursor()

    query = """
    SELECT id, arquivo, resumo, data_upload, categoria
    FROM exames
    ORDER BY data_upload DESC
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    exames = []

    for row in rows:

        exame = Exame(
            id=row[0],
            arquivo=row[1],
            resumo=row[2],
            data_upload=row[3],
            categoria=row[4]
        )

        exames.append(exame)

    return exames


def buscar_exame_por_id(exame_id):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, arquivo, texto, resumo, data_upload, categoria
        FROM exames
        WHERE id = ?
    """, (exame_id,))

    row = cursor.fetchone()

    if row is None:
        return None

    exame = Exame(
        id=row[0],
        arquivo=row[1],
        resumo=row[3],
        data_upload=row[4],
        categoria=row[5]
    )

    # adiciona texto dinamicamente para uso interno
    exame.texto = row[2]

    return exame


def excluir_exame(exame_id):
    """
    Remove um exame do banco e também remove o arquivo do sistema.
    """

    cursor = conn.cursor()

    cursor.execute("""
        SELECT arquivo
        FROM exames
        WHERE id = ?
    """, (exame_id,))

    resultado = cursor.fetchone()

    if resultado is None:
        return False

    nome_arquivo = resultado[0]

    cursor.execute("""
        DELETE FROM exames
        WHERE id = ?
    """, (exame_id,))

    conn.commit()

    caminho = os.path.join(UPLOAD_FOLDER, nome_arquivo)

    if os.path.exists(caminho):
        os.remove(caminho)

    return True


def montar_historico_exames():
    """
    Monta o histórico de exames em formato de texto
    para ser utilizado pelo chat de IA.
    """

    exames = listar_exames()

    historico = ""

    for exame in exames:

        historico += f"""
Categoria: {exame.categoria}
Arquivo: {exame.arquivo}
Data: {exame.data_upload}

Resumo:
{exame.resumo}

"""

    return historico


def buscar_exames_relevantes(pergunta):
    """
    Busca exames cujo texto ou resumo contenham palavras da pergunta.
    """

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, arquivo, texto, resumo, data_upload, categoria
        FROM exames
    """)

    rows = cursor.fetchall()

    pergunta = pergunta.lower()

    relevantes = []

    for row in rows:

        texto = (row[2] or "").lower()
        resumo = (row[3] or "").lower()

        if any(palavra in texto or palavra in resumo for palavra in pergunta.split()):

            exame = Exame(
                id=row[0],
                arquivo=row[1],
                resumo=row[3],
                data_upload=row[4],
                categoria=row[5]
            )

            exame.texto = row[2]

            relevantes.append(exame)

    return relevantes


def buscar_exame_por_nome(nome):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, arquivo, texto, resumo, data_upload, categoria
        FROM exames
        WHERE arquivo = ?
    """, (nome,))

    row = cursor.fetchone()

    if row is None:
        return None

    exame = Exame(
        id=row[0],
        arquivo=row[1],
        resumo=row[3],
        data_upload=row[4],
        categoria=row[5]
    )

    exame.texto = row[2]

    return exame

def montar_timeline_exames():
    """
    Organiza os exames por categoria e ano.
    Estrutura retornada:

    {
        "Hemograma": {
            "2026": [exame, exame]
        },
        "Colesterol": {
            "2025": [exame]
        }
    }
    """

    exames = listar_exames()

    timeline = {}

    for exame in exames:

        categoria = exame.categoria or "Outros"
        ano = exame.data_upload[:4]

        if categoria not in timeline:
            timeline[categoria] = {}

        if ano not in timeline[categoria]:
            timeline[categoria][ano] = []

        timeline[categoria][ano].append(exame)

    return timeline
