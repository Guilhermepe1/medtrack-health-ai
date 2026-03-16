from database.db import get_connection

def buscar_usuario_por_username(username):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, username, senha
        FROM usuarios
        WHERE username = ?
    """, (username,))

    conn.commit()
    conn.close()

    return cursor.fetchone()


def criar_usuario(nome, username, senha_hash):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usuarios (nome, username, senha)
        VALUES (?, ?, ?)
    """, (nome, username, senha_hash))

    conn.commit()
    conn.close()
