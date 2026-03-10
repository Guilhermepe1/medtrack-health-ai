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
        arquivo TEXT,
        texto TEXT,
        resumo TEXT,
        categoria TEXT,
        data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    try:
        cursor.execute("ALTER TABLE exames ADD COLUMN categoria TEXT")
    except:
        pass

    conn.commit()


# Inicializa banco ao carregar módulo
init_db()
