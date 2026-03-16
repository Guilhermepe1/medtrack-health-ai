from database.db import get_connection


def buscar_usuario_por_username(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, username, senha FROM usuarios WHERE username = %s",
        (username,)
    )

    usuario = cursor.fetchone()

    conn.close()

    return usuario


def criar_usuario(nome, username, senha):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO usuarios (nome, username, senha)
        VALUES (%s, %s, %s)
        """,
        (nome, username, senha)
    )

    conn.commit()
    conn.close()
