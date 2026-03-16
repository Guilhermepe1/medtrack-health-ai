"""
Conexão com PostgreSQL (Supabase)
"""

import psycopg2
import streamlit as st


def get_connection():

    conn = psycopg2.connect(
        host=st.secrets["DB_HOST"],
        database="postgres",
        user="postgres",
        password=st.secrets["DB_PASSWORD"],
        port=5432,
        sslmode="require"
    )

    return conn
