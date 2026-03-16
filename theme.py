"""
Tema visual do MedTrack Health AI.
Minimalista, claro, verde-saúde.
"""

import streamlit as st


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
        background-color: #F7F9F8;
    }

    .block-container {
        padding: 2rem 2.5rem 3rem 2.5rem !important;
        max-width: 960px !important;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E8EDEA;
        padding-top: 1.5rem;
    }

    [data-testid="stSidebar"] .block-container {
        padding: 1rem 1.2rem !important;
    }

    /* Logo na sidebar */
    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.5rem 0.2rem 1.5rem 0.2rem;
        border-bottom: 1px solid #E8EDEA;
        margin-bottom: 1.2rem;
    }

    .sidebar-logo-icon {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #2D9B6F, #1E7A54);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }

    .sidebar-logo-text {
        font-family: 'DM Serif Display', serif;
        font-size: 16px;
        color: #1A2E25;
        line-height: 1.2;
    }

    .sidebar-logo-sub {
        font-size: 11px;
        color: #6B8C7D;
        font-weight: 400;
    }

    /* Avatar do usuário na sidebar */
    .sidebar-user {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.8rem;
        background: #F0F7F4;
        border-radius: 12px;
        margin-bottom: 1.5rem;
    }

    .sidebar-avatar {
        width: 36px;
        height: 36px;
        background: linear-gradient(135deg, #2D9B6F, #1E7A54);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: 600;
        font-size: 14px;
        flex-shrink: 0;
    }

    .sidebar-username {
        font-size: 13px;
        font-weight: 500;
        color: #1A2E25;
    }

    .sidebar-tag {
        font-size: 11px;
        color: #6B8C7D;
    }

    /* Itens de navegação */
    .nav-item {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 0.65rem 0.8rem;
        border-radius: 10px;
        margin-bottom: 4px;
        cursor: pointer;
        font-size: 14px;
        font-weight: 400;
        color: #4A6B5C;
        transition: all 0.15s ease;
        text-decoration: none;
    }

    .nav-item:hover {
        background: #F0F7F4;
        color: #1A2E25;
    }

    .nav-item.active {
        background: #E8F5EF;
        color: #1E7A54;
        font-weight: 500;
    }

    .nav-icon {
        font-size: 16px;
        width: 20px;
        text-align: center;
    }

    /* ── Títulos ── */
    h1 {
        font-family: 'DM Serif Display', serif !important;
        color: #1A2E25 !important;
        font-size: 28px !important;
        font-weight: 400 !important;
        margin-bottom: 0.2rem !important;
    }

    h2 {
        font-family: 'DM Sans', sans-serif !important;
        color: #1A2E25 !important;
        font-size: 20px !important;
        font-weight: 600 !important;
    }

    h3 {
        color: #2D5A45 !important;
        font-size: 16px !important;
        font-weight: 500 !important;
    }

    /* ── Cards de métricas ── */
    .metric-card {
        background: #FFFFFF;
        border: 1px solid #E8EDEA;
        border-radius: 16px;
        padding: 1.2rem 1.4rem;
        transition: box-shadow 0.2s ease;
    }

    .metric-card:hover {
        box-shadow: 0 4px 16px rgba(45, 155, 111, 0.08);
    }

    .metric-label {
        font-size: 12px;
        font-weight: 500;
        color: #6B8C7D;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    .metric-value {
        font-size: 28px;
        font-weight: 600;
        color: #1A2E25;
        line-height: 1;
    }

    .metric-sub {
        font-size: 12px;
        color: #6B8C7D;
        margin-top: 4px;
    }

    .metric-icon {
        font-size: 20px;
        margin-bottom: 8px;
    }

    /* ── Cards de exames ── */
    .exame-card {
        background: #FFFFFF;
        border: 1px solid #E8EDEA;
        border-radius: 14px;
        padding: 1rem 1.2rem;
        margin-bottom: 10px;
        transition: all 0.15s ease;
    }

    .exame-card:hover {
        border-color: #A8D5BE;
        box-shadow: 0 2px 12px rgba(45, 155, 111, 0.06);
    }

    .exame-card-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 6px;
    }

    .exame-titulo {
        font-size: 14px;
        font-weight: 500;
        color: #1A2E25;
    }

    .exame-data {
        font-size: 12px;
        color: #6B8C7D;
    }

    .exame-resumo {
        font-size: 13px;
        color: #4A6B5C;
        line-height: 1.5;
    }

    /* Badges de categoria */
    .badge {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 500;
    }

    .badge-verde  { background: #E8F5EF; color: #1E7A54; }
    .badge-azul   { background: #EBF4FF; color: #1A5FAB; }
    .badge-laranja{ background: #FFF3E8; color: #B85C00; }
    .badge-cinza  { background: #F0F2F1; color: #4A6B5C; }

    /* ── Alertas clínicos ── */
    .alerta-card {
        background: #FFFFFF;
        border-left: 4px solid #E84545;
        border-radius: 0 12px 12px 0;
        padding: 0.9rem 1.2rem;
        margin-bottom: 8px;
        border-top: 1px solid #F5E0E0;
        border-right: 1px solid #F5E0E0;
        border-bottom: 1px solid #F5E0E0;
    }

    .alerta-card.baixo {
        border-left-color: #3B82F6;
        border-top-color: #E0EAFF;
        border-right-color: #E0EAFF;
        border-bottom-color: #E0EAFF;
    }

    .alerta-parametro {
        font-size: 14px;
        font-weight: 500;
        color: #1A2E25;
    }

    .alerta-valor {
        font-size: 13px;
        color: #4A6B5C;
        margin-top: 2px;
    }

    /* ── Botões ── */
    .stButton > button {
        background-color: #2D9B6F !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.2rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        font-size: 14px !important;
        transition: all 0.15s ease !important;
    }

    .stButton > button:hover {
        background-color: #1E7A54 !important;
        box-shadow: 0 4px 12px rgba(45, 155, 111, 0.25) !important;
        transform: translateY(-1px) !important;
    }

    .stButton > button[kind="secondary"] {
        background-color: transparent !important;
        color: #2D9B6F !important;
        border: 1px solid #A8D5BE !important;
    }

    .stButton > button[kind="secondary"]:hover {
        background-color: #F0F7F4 !important;
    }

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 1px solid #D4E0DA !important;
        background: #FFFFFF !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
        color: #1A2E25 !important;
        transition: border-color 0.15s ease !important;
    }

    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #2D9B6F !important;
        box-shadow: 0 0 0 3px rgba(45, 155, 111, 0.12) !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 1px solid #D4E0DA !important;
        background: #FFFFFF !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
    }

    /* ── File uploader ── */
    [data-testid="stFileUploader"] {
        border: 2px dashed #A8D5BE !important;
        border-radius: 14px !important;
        background: #F7FCF9 !important;
        padding: 1rem !important;
    }

    /* ── Chat input ── */
    [data-testid="stChatInput"] textarea {
        border-radius: 14px !important;
        border: 1px solid #D4E0DA !important;
        background: #FFFFFF !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Mensagens do chat ── */
    [data-testid="stChatMessage"] {
        background: #FFFFFF !important;
        border: 1px solid #E8EDEA !important;
        border-radius: 14px !important;
        padding: 0.8rem 1rem !important;
        margin-bottom: 8px !important;
    }

    /* ── Divider ── */
    hr {
        border-color: #E8EDEA !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Notificação de alertas ── */
    .stAlert {
        border-radius: 12px !important;
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border-radius: 12px !important;
        overflow: hidden !important;
        border: 1px solid #E8EDEA !important;
    }

    /* ── Esconde elementos padrão do Streamlit ── */
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }

    /* ── Page header customizado ── */
    .page-header {
        margin-bottom: 1.5rem;
    }

    .page-title {
        font-family: 'DM Serif Display', serif;
        font-size: 24px;
        color: #1A2E25;
        margin: 0;
        line-height: 1.2;
    }

    .page-subtitle {
        font-size: 13px;
        color: #6B8C7D;
        margin-top: 4px;
    }
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


def badge(texto, tipo="verde"):
    st.markdown(
        f'<span class="badge badge-{tipo}">{texto}</span>',
        unsafe_allow_html=True
    )


def sidebar_logo():
    st.sidebar.markdown("""
    <div class="sidebar-logo">
        <div class="sidebar-logo-icon">🩺</div>
        <div>
            <div class="sidebar-logo-text">MedTrack</div>
            <div class="sidebar-logo-sub">Health AI</div>
        </div>
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
