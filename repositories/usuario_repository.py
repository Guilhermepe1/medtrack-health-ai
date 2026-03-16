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


def buscar_usuario_por_google_id(google_id):

    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute(
        "SELECT id, nome, username, email FROM usuarios WHERE google_id = %s",
        (google_id,)
    )

    usuario = cursor.fetchone()
    conn.close()

    return usuario


def buscar_usuario_por_email(email):

    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute(
        "SELECT id, nome, username, email, google_id FROM usuarios WHERE email = %s",
        (email,)
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


def criar_usuario_google(nome, username, email, google_id, avatar_url=None):
    """
    Cria um usuário autenticado via Google (sem senha).
    """
    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute(
        """
        INSERT INTO usuarios (nome, username, email, google_id, avatar_url)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """,
        (nome, username, email, google_id, avatar_url)
    )

    row = cursor.fetchone()
    conn.commit()
    conn.close()

    return row["id"]


def vincular_google_id(usuario_id, google_id, email, avatar_url=None):
    """
    Vincula um Google ID a um usuário existente (login tradicional).
    """
    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute(
        """
        UPDATE usuarios
        SET google_id = %s, email = %s, avatar_url = %s
        WHERE id = %s
        """,
        (google_id, email, avatar_url, usuario_id)
    )

    conn.commit()
    conn.close()