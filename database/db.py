"""
Conexão com PostgreSQL (Supabase)
"""

import psycopg2
import streamlit as st


def get_connection():

    DATABASE_URL = st.secrets["DATABASE_URL"]

    conn = psycopg2.connect(DATABASE_URL)

    return conn
