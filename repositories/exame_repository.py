"""
Repository responsável por todas as operações no banco
relacionadas à entidade Exame.
"""

import os
from database.db import get_connection, get_cursor
from models.exame import Exame

UPLOAD_FOLDER = "uploads"


def salvar_exame(usuario_id, arquivo, texto, resumo, categoria):
    """
    Salva um novo exame no banco de dados.
    """

    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute(
        """
        INSERT INTO exames (usuario_id, arquivo, texto, resumo, categoria)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (usuario_id, arquivo, texto, resumo, categoria)
    )

    conn.commit()
    conn.close()


def listar_exames(usuario_id):

    conn = get_connection()
    cursor = get_cursor(conn)

    query = """
    SELECT id, arquivo, resumo, data_upload, categoria
    FROM exames
    WHERE usuario_id = %s
    ORDER BY data_upload DESC
    """

    cursor.execute(query, (usuario_id,))
    rows = cursor.fetchall()
    conn.close()

    exames = []

    for row in rows:
        exame = Exame(
            id=row["id"],
            arquivo=row["arquivo"],
            resumo=row["resumo"],
            data_upload=str(row["data_upload"]),
            categoria=row["categoria"]
        )
        exames.append(exame)

    return exames


def buscar_exame_por_id(exame_id):

    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute("""
        SELECT id, arquivo, texto, resumo, data_upload, categoria
        FROM exames
        WHERE id = %s
    """, (exame_id,))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    exame = Exame(
        id=row["id"],
        arquivo=row["arquivo"],
        resumo=row["resumo"],
        data_upload=str(row["data_upload"]),
        categoria=row["categoria"]
    )
    exame.texto = row["texto"]

    return exame


def excluir_exame(exame_id):
    """
    Remove um exame do banco e também remove o arquivo do sistema.
    """

    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute("""
        SELECT arquivo
        FROM exames
        WHERE id = %s
    """, (exame_id,))

    resultado = cursor.fetchone()

    if resultado is None:
        conn.close()
        return False

    nome_arquivo = resultado["arquivo"]

    cursor.execute("""
        DELETE FROM exames
        WHERE id = %s
    """, (exame_id,))

    conn.commit()
    conn.close()

    caminho = os.path.join(UPLOAD_FOLDER, nome_arquivo)

    if os.path.exists(caminho):
        os.remove(caminho)

    return True


def montar_historico_exames(usuario_id):
    """
    Monta o histórico de exames em formato de texto
    para ser utilizado pelo chat de IA.
    """

    exames = listar_exames(usuario_id)

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


def buscar_exames_relevantes(usuario_id, pergunta):
    """
    Busca exames relevantes apenas do usuário.
    """

    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute("""
        SELECT id, arquivo, texto, resumo, data_upload, categoria
        FROM exames
        WHERE usuario_id = %s
    """, (usuario_id,))

    rows = cursor.fetchall()
    conn.close()

    pergunta = pergunta.lower()
    relevantes = []

    for row in rows:
        texto = (row["texto"] or "").lower()
        resumo = (row["resumo"] or "").lower()

        if any(palavra in texto or palavra in resumo for palavra in pergunta.split()):
            exame = Exame(
                id=row["id"],
                arquivo=row["arquivo"],
                resumo=row["resumo"],
                data_upload=str(row["data_upload"]),
                categoria=row["categoria"]
            )
            exame.texto = row["texto"]
            relevantes.append(exame)

    return relevantes


def buscar_exame_por_nome(usuario_id, nome):

    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute("""
        SELECT id, arquivo, texto, resumo, data_upload, categoria
        FROM exames
        WHERE usuario_id = %s AND arquivo = %s
    """, (usuario_id, nome))

    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None

    exame = Exame(
        id=row["id"],
        arquivo=row["arquivo"],
        resumo=row["resumo"],
        data_upload=str(row["data_upload"]),
        categoria=row["categoria"]
    )
    exame.texto = row["texto"]

    return exame


def montar_timeline_exames(usuario_id):
    """
    Organiza os exames por categoria e ano.
    """

    exames = listar_exames(usuario_id)

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