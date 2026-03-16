"""
Conexão com banco PostgreSQL (Supabase)
"""

import os
import psycopg2
import streamlit as st


def get_connection():

    DATABASE_URL = st.secrets["DATABASE_URL"]

    conn = psycopg2.connect(DATABASE_URL)

    return conn
