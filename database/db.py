import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st


def get_connection():
    conn = psycopg2.connect(
        host=st.secrets["DB_HOST"],
        database="postgres",
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        port=5432,
        sslmode="require"
    )
    return conn


def get_cursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)