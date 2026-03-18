"""
Aplicação principal do MedTrack Health AI.
"""

import streamlit as st
from datetime import datetime

from auth.login_ui import render_login
from ui.dashboard_ui import render_dashboard
from ui.upload_ui import render_upload
from ui.timeline_ui import render_timeline
from ui.chat_ui import render_chat
from ui.valores_ui import render_valores
from ui.alertas_ui import render_alertas
from ui.perfil_ui import render_avatar_sidebar, render_modal_perfil
from ui.odonto_ui import render_odonto
from ui.lgpd_ui import render_termo_consentimento, render_painel_privacidade
from ui.minha_conta_ui import render_minha_conta
from ui.compartilhar_ui import render_compartilhar
from repositories.link_medico_repository import buscar_link_valido, registrar_acesso
from services.relatorio_service import gerar_pdf_medico
from ui.compartilhar_ui import render_compartilhar
from repositories.alertas_repository import buscar_alertas_nao_lidos
from repositories.lgpd_repository import registrar_log
from theme import aplicar_tema, sidebar_logo, page_header

st.set_page_config(
    page_title="MedTrack Health AI",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


def get_saudacao():
    hora = datetime.now().hour
    if hora < 12:
        return "Bom dia"
    elif hora < 18:
        return "Boa tarde"
    return "Boa noite"


def render_sidebar():
    sidebar_logo()
    render_avatar_sidebar(st.session_state["usuario_nome"])

    nao_lidos    = buscar_alertas_nao_lidos(st.session_state["usuario_id"])
    alerta_badge = f" 🔴 {len(nao_lidos)}" if nao_lidos else ""

    if "pagina" not in st.session_state:
        st.session_state["pagina"] = "dashboard"

    st.sidebar.markdown(
        '<div class="nav-label">Saúde Geral</div>',
        unsafe_allow_html=True
    )

    paginas_geral = {
        "dashboard": ("🏠", "Início"),
        "upload":    ("📤", "Enviar Exame"),
        "timeline":  ("🗂️", "Meus Exames"),
        "valores":   ("📊", "Valores Laboratoriais"),
        "alertas":   ("⚠️", f"Alertas{alerta_badge}"),
        "chat":      ("💬", "Chat de Saúde"),
    }

    for key, (icone, label) in paginas_geral.items():
        ativo = st.session_state["pagina"] == key
        if st.sidebar.button(
            f"{icone}  {label}",
            key=f"nav_{key}",
            use_container_width=True,
            type="primary" if ativo else "secondary"
        ):
            st.session_state["pagina"] = key
            st.session_state["modal_perfil"] = False
            st.rerun()

    st.sidebar.markdown(
        '<div class="nav-label" style="margin-top:12px">Saúde Bucal</div>',
        unsafe_allow_html=True
    )

    ativo_odonto = st.session_state["pagina"] == "odonto"
    if st.sidebar.button(
        "🦷  Odontológico",
        key="nav_odonto",
        use_container_width=True,
        type="primary" if ativo_odonto else "secondary"
    ):
        st.session_state["pagina"] = "odonto"
        st.session_state["modal_perfil"] = False
        st.rerun()

    st.sidebar.markdown(
        '<div class="nav-label" style="margin-top:12px">Conta</div>',
        unsafe_allow_html=True
    )

    ativo_compartilhar = st.session_state["pagina"] == "compartilhar"
    if st.sidebar.button(
        "🩺  Compartilhar com médico",
        key="nav_compartilhar",
        use_container_width=True,
        type="primary" if ativo_compartilhar else "secondary"
    ):
        st.session_state["pagina"] = "compartilhar"
        st.session_state["modal_perfil"] = False
        st.rerun()

    ativo_compartilhar = st.session_state["pagina"] == "compartilhar"
    if st.sidebar.button(
        "🩺  Compartilhar com médico",
        key="nav_compartilhar",
        use_container_width=True,
        type="primary" if ativo_compartilhar else "secondary"
    ):
        st.session_state["pagina"] = "compartilhar"
        st.session_state["modal_perfil"] = False
        st.rerun()

    ativo_conta = st.session_state["pagina"] == "minha_conta"
    if st.sidebar.button(
        "👤  Minha Conta",
        key="nav_minha_conta",
        use_container_width=True,
        type="primary" if ativo_conta else "secondary"
    ):
        st.session_state["pagina"] = "minha_conta"
        st.session_state["modal_perfil"] = False
        st.rerun()

    ativo_privacidade = st.session_state["pagina"] == "privacidade"
    if st.sidebar.button(
        "🔒  Privacidade e LGPD",
        key="nav_privacidade",
        use_container_width=True,
        type="primary" if ativo_privacidade else "secondary"
    ):
        st.session_state["pagina"] = "privacidade"
        st.session_state["modal_perfil"] = False
        st.rerun()

    st.sidebar.divider()

    if st.sidebar.button("🚪  Sair", use_container_width=True, type="secondary"):
        registrar_log(
            st.session_state["usuario_id"],
            "logout",
            "Usuário encerrou sessão"
        )
        st.session_state.clear()
        st.rerun()



def _render_view_medico(token):
    """Exibe o relatório para o médico via link temporário."""
    from datetime import datetime
    aplicar_tema()

    link = buscar_link_valido(token)
    if not link:
        st.error("❌ Link inválido ou expirado.")
        st.caption("Peça ao paciente que gere um novo link no MedTrack.")
        return

    registrar_acesso(token)

    st.markdown("## 🩺 Relatório de Saúde — MedTrack Health AI")
    st.caption(
        f"Acesso somente leitura · "
        f"Válido até {str(link['expira_em'])[:16]}"
    )
    st.divider()

    pdf_bytes = gerar_pdf_medico(link["usuario_id"])
    nome = f"relatorio_medtrack_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"

    st.info(
        "Este relatório foi compartilhado pelo paciente para esta consulta. "
        "Clique abaixo para baixar o PDF completo."
    )

    st.download_button(
        label="⬇️ Baixar relatório PDF",
        data=pdf_bytes,
        file_name=nome,
        mime="application/pdf",
        use_container_width=True,
    )

    st.caption(
        "MedTrack Health AI — Documento gerado automaticamente. "
        "Não substitui avaliação médica profissional."
    )


def main():

    aplicar_tema()

    # intercepta link de médico na URL
    params = st.query_params
    if "medico" in params:
        _render_view_medico(params["medico"])
        return

    if "logado" not in st.session_state:
        render_login()
        return

    if not render_termo_consentimento():
        return

    render_sidebar()

    if st.session_state.get("modal_perfil"):
        render_modal_perfil()
        return

    pagina   = st.session_state.get("pagina", "dashboard")
    nome     = st.session_state["usuario_nome"]
    saudacao = get_saudacao()

    if pagina == "dashboard":
        page_header(
            f"{saudacao}, {nome} 👋",
            "Aqui está um resumo da sua saúde hoje"
        )
        render_dashboard()

    elif pagina == "upload":
        page_header("Enviar Exame", "Envie um novo exame para análise automática")
        render_upload()

    elif pagina == "timeline":
        page_header("Meus Exames", "Histórico completo dos seus exames")
        render_timeline()

    elif pagina == "valores":
        page_header("Valores Laboratoriais",
                    "Acompanhe a evolução dos seus indicadores")
        render_valores()

    elif pagina == "alertas":
        page_header("Alertas Clínicos", "Valores que merecem atenção")
        render_alertas()

    elif pagina == "chat":
        page_header("Chat de Saúde",
                    "Tire dúvidas sobre seus exames com IA")
        render_chat()

    elif pagina == "odonto":
        page_header("Saúde Bucal",
                    "Odontograma, radiografias e histórico odontológico")
        render_odonto()

    elif pagina == "compartilhar":
        page_header("Compartilhar com Médico",
                    "Link seguro e relatório PDF para sua consulta")
        render_compartilhar()

    elif pagina == "compartilhar":
        page_header("Compartilhar com Médico",
                    "Link seguro e temporário para sua consulta")
        render_compartilhar()

    elif pagina == "minha_conta":
        page_header("Minha Conta", "Visualize e edite seus dados cadastrais")
        render_minha_conta()

    elif pagina == "privacidade":
        page_header("Privacidade e LGPD", "Seus dados, seus direitos")
        render_painel_privacidade()


if __name__ == "__main__":
    main()