from database.db import get_connection, get_cursor


def buscar_usuario_por_username(username):

    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute(
        "SELECT id, nome, username, senha FROM usuarios WHERE username = %s",
        (username,)
    )

    usuario = cursor.fetchone()
    conn.close()

    return usuario


def criar_usuario(nome, username, senha):

    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute(
        """
        INSERT INTO usuarios (nome, username, senha)
        VALUES (%s, %s, %s)
        """,
        (nome, username, senha)
    )

    conn.commit()
    conn.close()