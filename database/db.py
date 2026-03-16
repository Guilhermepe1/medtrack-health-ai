import psycopg2
import streamlit as st


def get_connection():

    conn = psycopg2.connect(
        host="aws-1-sa-east-1.pooler.supabase.com",
        database="postgres",
        user="postgres.uhlzssxjspylffpriaqt",
        password=st.secrets["DB_PASSWORD"],
        port=5432,
        sslmode="require"
    )

    return conn
