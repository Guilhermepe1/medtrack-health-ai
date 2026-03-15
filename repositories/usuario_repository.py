from database.db import conn


def buscar_usuario_por_username(username):

    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, username, senha
        FROM usuarios
        WHERE username = ?
    """, (username,))

    return cursor.fetchone()


def criar_usuario(nome, username, senha_hash):

    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usuarios (nome, username, senha)
        VALUES (?, ?, ?)
    """, (nome, username, senha_hash))

    conn.commit()
