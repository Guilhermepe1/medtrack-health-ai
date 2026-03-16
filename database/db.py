"""
Conexão com PostgreSQL (Supabase)
"""

import psycopg2
import streamlit as st


def get_connection():

    conn = psycopg2.connect(
        host=st.secrets["db.uhlzssxjspylffpriaqt.supabase.co"],
        database="postgres",
        user="postgres",
        password=st.secrets["/6$B%3Awa3A+Ecy"],
        port=5432,
        sslmode="require"
    )

    return conn
