"""
database/db.py

Responsável por:
- Criar conexão com o banco SQLite
- Inicializar as tabelas do sistema
"""

import sqlite3

# Caminho do banco de dados
DB_NAME = "exames.db"

# Cria conexão global com o banco
conn = sqlite3.connect(DB_NAME, check_same_thread=False)

# Cursor para executar queries
cursor = conn.cursor()


def init_db():
    """
    Inicializa o banco de dados criando as tabelas necessárias
    caso ainda não existam.
    """

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS exames (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        usuario_id INTEGER,
        arquivo TEXT,
        texto TEXT,
        resumo TEXT,
        categoria TEXT,
        data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # garantir que a coluna usuario_id exista (migração automática)

    cursor.execute("PRAGMA table_info(exames)")
    colunas = [coluna[1] for coluna in cursor.fetchall()]

    if "usuario_id" not in colunas:
        cursor.execute("ALTER TABLE exames ADD COLUMN usuario_id INTEGER")


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        username TEXT UNIQUE,
        senha TEXT
    )
    """)


    try:
        cursor.execute("ALTER TABLE exames ADD COLUMN categoria TEXT")
    except:
        pass

    conn.commit()


# Inicializa banco ao carregar módulo
init_db()
