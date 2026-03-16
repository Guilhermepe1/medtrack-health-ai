"""
Tema visual do MedTrack Health AI.
Paleta baseada na logo: teal #00C9A7, azul #2B7FD4, marinho #1A2A6C.
"""

import base64
import streamlit as st


def _logo_base64():
    try:
        with open("logo-medtrack.png", "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None


def aplicar_tema():
    st.markdown("""
    <style>
    /* ── Fontes ── */
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Serif+Display&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    /* ── Fundo e layout geral ── */
    .stApp {
        background-color: #F4F8FC;
    }

    .block-container {
        padding: 2rem 2.5rem 3rem 2.5rem !important;
        max-width: 960px !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1A2A6C 0%, #1D3A8A 60%, #1A4A7A 100%);
        border-right: none;
        padding-top: 0;
    }

    [data-testid="stSidebar"] .block-container {
        padding: 0 !important;
    }

    /* ── Logo na sidebar ── */
    .sidebar-logo-wrap {
        padding: 1.6rem 1.2rem 1.2rem 1.2rem;
        border-bottom: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 1rem;
        text-align: center;
    }

    .sidebar-logo-wrap img {
        width: 120px;
        margin-bottom: 4px;
    }

    .sidebar-logo-sub {
        font-size: 11px;
        color: rgba(255,255,255,0.5);
        letter-spacing: 1.5px;
        text-transform: uppercase;
    }

    /* ── Avatar do usuário ── */
    .sidebar-user {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.7rem 1rem;
        background: rgba(255,255,255,0.08);
        border-radius: 12px;
        margin: 0 1rem 1.2rem 1rem;
    }

    .sidebar-avatar {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #00C9A7, #2B7FD4);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 15px;
        flex-shrink: 0;
    }

    .sidebar-username {
        font-size: 13px;
        font-weight: 500;
        color: #FFFFFF;
    }

    .sidebar-tag {
        font-size: 11px;
        color: rgba(255,255,255,0.5);
    }

    /* ── Label do menu ── */
    .nav-label {
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: rgba(255,255,255,0.4);
        padding: 0 1.2rem;
        margin-bottom: 6px;
    }

    /* ── Botões da sidebar ── */
    [data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        color: rgba(255,255,255,0.75) !important;
        border: none !important;
        border-radius: 10px !important;
        text-align: left !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        padding: 0.6rem 1rem !important;
        width: 100% !important;
        transition: all 0.15s ease !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.1) !important;
        color: #FFFFFF !important;
        transform: none !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(0,201,167,0.25), rgba(43,127,212,0.25)) !important;
        color: #FFFFFF !important;
        border-left: 3px solid #00C9A7 !important;
        font-weight: 500 !important;
    }

    /* ── Títulos ── */
    h1 {
        font-family: 'DM Serif Display', serif !important;
        color: #1A2A6C !important;
        font-size: 28px !important;
        font-weight: 400 !important;
        margin-bottom: 0.2rem !important;
    }

    h2 {
        color: #1A2A6C !important;
        font-size: 20px !important;
        font-weight: 600 !important;
    }

    h3 {
        color: #1D3A8A !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }

    /* ── Cards ── */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E0EAF5;
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        transition: box-shadow 0.2s ease;
    }

    .metric-card:hover {
        box-shadow: 0 4px 20px rgba(43, 127, 212, 0.10);
    }

    .metric-label {
        font-size: 11px;
        font-weight: 600;
        color: #6B8CB0;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 600;
        color: #1A2A6C;
        line-height: 1;
    }

    .metric-sub {
        font-size: 12px;
        color: #6B8CB0;
        margin-top: 4px;
    }

    .metric-icon { font-size: 20px; margin-bottom: 8px; }

    /* ── Page header ── */
    .page-header { margin-bottom: 1.5rem; }

    .page-title {
        font-family: 'DM Serif Display', serif;
        font-size: 26px;
        color: #1A2A6C;
        margin: 0;
        line-height: 1.2;
    }

    .page-subtitle {
        font-size: 13px;
        color: #6B8CB0;
        margin-top: 4px;
    }

    /* ── Badges ── */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 500;
    }

    .badge-teal   { background: #E0FAF6; color: #00897B; }
    .badge-azul   { background: #E3EFFC; color: #1A5FAB; }
    .badge-marinho{ background: #E8EBF8; color: #1A2A6C; }
    .badge-cinza  { background: #F0F2F5; color: #4A6080; }

    /* ── Alertas clínicos ── */
    .alerta-card {
        background: #FFFFFF;
        border-left: 4px solid #E84545;
        border-radius: 0 12px 12px 0;
        padding: 0.9rem 1.2rem;
        margin-bottom: 8px;
        border-top: 1px solid #FAE8E8;
        border-right: 1px solid #FAE8E8;
        border-bottom: 1px solid #FAE8E8;
    }

    .alerta-card.baixo {
        border-left-color: #2B7FD4;
        border-top-color: #E3EFFC;
        border-right-color: #E3EFFC;
        border-bottom-color: #E3EFFC;
    }

    /* ── Botões principais ── */
    .stButton > button {
        background: linear-gradient(135deg, #00C9A7, #2B7FD4) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.2rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        opacity: 0.9 !important;
        box-shadow: 0 4px 16px rgba(43, 127, 212, 0.3) !important;
        transform: translateY(-1px) !important;
    }

    .stButton > button[kind="secondary"] {
        background: transparent !important;
        color: #2B7FD4 !important;
        border: 1px solid #B0CFF0 !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background: #E3EFFC !important;
        transform: none !important;
        box-shadow: none !important;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 1px solid #C8DAEA !important;
        background: #FFFFFF !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
        color: #1A2A6C !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #2B7FD4 !important;
        box-shadow: 0 0 0 3px rgba(43, 127, 212, 0.12) !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 1px solid #C8DAEA !important;
        background: #FFFFFF !important;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        border: 2px dashed #8BBFE8 !important;
        border-radius: 14px !important;
        background: #F0F6FC !important;
    }

    /* ── Chat ── */
    [data-testid="stChatInput"] textarea {
        border-radius: 14px !important;
        border: 1px solid #C8DAEA !important;
        background: #FFFFFF !important;
    }

    [data-testid="stChatMessage"] {
        background: #FFFFFF !important;
        border: 1px solid #E0EAF5 !important;
        border-radius: 14px !important;
    }

    /* ── Divider ── */
    hr { border-color: #E0EAF5 !important; }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border-radius: 12px !important;
        border: 1px solid #E0EAF5 !important;
        overflow: hidden !important;
    }

    /* ── Esconde elementos padrão ── */
    #MainMenu { visibility: hidden; }
    footer     { visibility: hidden; }
    header     { visibility: hidden; }
    </style>
    """, unsafe_allow_html=True)


def card_metrica(icone, label, valor, sub=None):
    sub_html = f'<div class="metric-sub">{sub}</div>' if sub else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-icon">{icone}</div>
        <div class="metric-label">{label}</div>
        <div class="metric-value">{valor}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def page_header(titulo, subtitulo=None):
    sub_html = f'<div class="page-subtitle">{subtitulo}</div>' if subtitulo else ""
    st.markdown(f"""
    <div class="page-header">
        <div class="page-title">{titulo}</div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def badge(texto, tipo="teal"):
    st.markdown(
        f'<span class="badge badge-{tipo}">{texto}</span>',
        unsafe_allow_html=True
    )


def sidebar_logo():
    logo_b64 = _logo_base64()

    if logo_b64:
        img_html = f'<img src="data:image/png;base64,{logo_b64}" />'
    else:
        img_html = '<div style="font-size:32px;margin-bottom:4px;">🩺</div>'

    st.sidebar.markdown(f"""
    <div class="sidebar-logo-wrap">
        {img_html}
        <div class="sidebar-logo-sub">Health AI</div>
    </div>
    """, unsafe_allow_html=True)


def sidebar_usuario(nome):
    inicial = nome[0].upper() if nome else "?"
    st.sidebar.markdown(f"""
    <div class="sidebar-user">
        <div class="sidebar-avatar">{inicial}</div>
        <div>
            <div class="sidebar-username">{nome}</div>
            <div class="sidebar-tag">Paciente</div>
        </div>
    </div>
    """, unsafe_allow_html=True)