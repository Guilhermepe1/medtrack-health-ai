"""
UI de compartilhamento com médico.
Gera link temporário (24h) e PDF do relatório de saúde.
"""

import streamlit as st
from datetime import datetime

from repositories.link_medico_repository import (
    criar_link,
    buscar_link_valido,
    revogar_links,
    listar_links_usuario,
)
from services.relatorio_service import gerar_pdf_relatorio


def _tempo_restante(expira_em):
    """Retorna string legível do tempo restante."""
    delta = expira_em - datetime.now()
    total = int(delta.total_seconds())
    if total <= 0:
        return "Expirado"
    horas   = total // 3600
    minutos = (total % 3600) // 60
    if horas > 0:
        return f"{horas}h {minutos}min restantes"
    return f"{minutos} minutos restantes"


def _url_app():
    return "https://medtrack-health-ai-jqysifeyyr5akvkgaxlnp5.streamlit.app"


def render_compartilhar():
    usuario_id = st.session_state["usuario_id"]

    st.markdown(
        "Gere um link seguro e temporário para compartilhar seu histórico "
        "de saúde com seu médico durante a consulta. O link expira em **24 horas** "
        "e pode ser revogado a qualquer momento."
    )

    st.divider()

    # ── Link ativo ──
    link_ativo = buscar_link_valido(
        # busca pelo token mais recente do usuário
        _buscar_token_ativo(usuario_id)
    ) if _buscar_token_ativo(usuario_id) else None

    if link_ativo:
        token  = _buscar_token_ativo(usuario_id)
        url    = f"{_url_app()}/?token={token}"
        tempo  = _tempo_restante(link_ativo["expira_em"])
        acesso = link_ativo.get("acessado_em")

        st.success(f"✅ Você tem um link ativo — {tempo}")

        st.markdown("#### 🔗 Link para o médico")
        st.code(url, language=None)

        col1, col2 = st.columns(2)
        with col1:
            expira_fmt = link_ativo["expira_em"].strftime("%d/%m %H:%M")
            st.metric("Expira em", expira_fmt)
        with col2:
            acesso_fmt = acesso.strftime("%d/%m %H:%M") if acesso else "Ainda não acessado"
            st.metric("Último acesso", acesso_fmt)

        st.divider()

        col_novo, col_revogar = st.columns(2)

        with col_novo:
            if st.button("🔄 Gerar novo link", use_container_width=True):
                criar_link(usuario_id, horas=24)
                st.success("Novo link gerado!")
                st.rerun()

        with col_revogar:
            if st.button(
                "🚫 Revogar link",
                use_container_width=True,
                type="secondary"
            ):
                revogar_links(usuario_id)
                st.warning("Link revogado. O médico não conseguirá mais acessar.")
                st.rerun()

    else:
        st.info("Você não tem nenhum link ativo no momento.")

        if st.button("🔗 Gerar link para médico", use_container_width=True):
            criar_link(usuario_id, horas=24)
            st.success("Link gerado com sucesso!")
            st.rerun()

    st.divider()

    # ── Download do PDF ──
    st.markdown("#### 📄 Relatório em PDF")
    st.caption(
        "Baixe um PDF formatado com seus dados pessoais, perfil de saúde "
        "e histórico de exames para levar à consulta."
    )

    if st.button("📥 Gerar e baixar PDF", use_container_width=True):
        with st.spinner("Gerando relatório..."):
            try:
                pdf_bytes   = gerar_pdf_relatorio(usuario_id)
                nome_arquivo = (
                    f"relatorio_medtrack_"
                    f"{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
                )
                st.download_button(
                    label="⬇️ Clique aqui para baixar o PDF",
                    data=pdf_bytes,
                    file_name=nome_arquivo,
                    mime="application/pdf",
                    use_container_width=True,
                )
            except Exception as e:
                st.error(f"Erro ao gerar o PDF: {e}")
                st.caption(
                    "Verifique se o `reportlab` está instalado: "
                    "`pip install reportlab`"
                )

    st.divider()

    # ── Histórico de links ──
    historico = listar_links_usuario(usuario_id)

    if historico:
        st.markdown("#### 🕓 Histórico de links gerados")

        for link in historico:
            expirado   = link["expira_em"] < datetime.now()
            criado     = link["created_at"].strftime("%d/%m/%Y %H:%M")
            expira     = link["expira_em"].strftime("%d/%m/%Y %H:%M")
            acesso     = link.get("acessado_em")
            acesso_str = acesso.strftime("%d/%m %H:%M") if acesso else "Não acessado"

            if expirado:
                status = "⏰ Expirado"
                cor    = "#B85C00"
            else:
                status = "✅ Ativo"
                cor    = "#00C9A7"

            st.markdown(f"""
            <div style="
                background:#FFFFFF;
                border:1px solid #E0EAF5;
                border-left:3px solid {cor};
                border-radius:0 10px 10px 0;
                padding:0.6rem 1rem;
                margin-bottom:6px;
                font-size:12px;
                color:#1A2A6C;
            ">
                <span style="color:{cor};font-weight:600">{status}</span>
                &nbsp;·&nbsp; Criado: {criado}
                &nbsp;·&nbsp; Expira: {expira}
                &nbsp;·&nbsp; Acesso: {acesso_str}
            </div>
            """, unsafe_allow_html=True)


def _buscar_token_ativo(usuario_id):
    """
    Busca o token mais recente e válido do usuário consultando o histórico.
    """
    from repositories.link_medico_repository import listar_links_usuario
    from datetime import datetime

    links = listar_links_usuario(usuario_id)
    for link in links:
        if link["expira_em"] > datetime.now():
            return link["token"]
    return None