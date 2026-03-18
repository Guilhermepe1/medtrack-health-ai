"""
UI para geração de link seguro de compartilhamento com médico.
"""

import streamlit as st
from datetime import datetime

from repositories.link_medico_repository import (
    criar_link,
    listar_links_usuario,
    revogar_links,
)
from services.relatorio_service import gerar_pdf_medico


def _fmt(d):
    if not d:
        return "—"
    try:
        return datetime.strptime(str(d)[:16], "%Y-%m-%d %H:%M").strftime(
            "%d/%m/%Y às %H:%M"
        )
    except Exception:
        return str(d)[:16]


def _url_base():
    try:
        return st.secrets.get("APP_URL", "http://localhost:8501")
    except Exception:
        return "http://localhost:8501"


def render_compartilhar():
    usuario_id = st.session_state["usuario_id"]

    st.markdown(
        "Gere um link seguro com validade de **24 horas** para compartilhar "
        "seu histórico de saúde com seu médico durante a consulta."
    )
    st.info(
        "🔒 O link dá acesso somente leitura a: dados pessoais básicos, "
        "perfil de saúde e resumo dos exames. "
        "Nenhuma alteração pode ser feita por quem acessa o link."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Gerar novo link")

        if st.button("🔗 Gerar link para médico", use_container_width=True):
            with st.spinner("Gerando link seguro..."):
                token = criar_link(usuario_id, horas=24)
                url   = f"{_url_base()}/?medico={token}"
            st.session_state["link_gerado"] = url
            st.success("Link gerado com sucesso!")

        if st.session_state.get("link_gerado"):
            url = st.session_state["link_gerado"]
            st.markdown(f"""
            <div style="background:#E8F5EF;border:1px solid #A8D5BE;
                border-radius:10px;padding:12px 14px;margin-top:8px;
                word-break:break-all;font-size:12px;color:#1E7A54;">
                🔗 {url}
            </div>
            """, unsafe_allow_html=True)
            st.caption("Copie o link acima e envie para seu médico.")

            if st.button("🗑️ Revogar link", type="secondary",
                         use_container_width=True):
                revogar_links(usuario_id)
                st.session_state.pop("link_gerado", None)
                st.success("Link revogado.")
                st.rerun()

    with col2:
        st.markdown("#### Baixar PDF do relatório")
        st.caption("Prefere levar um documento impresso? Baixe o PDF aqui.")

        if st.button("📄 Gerar PDF", use_container_width=True):
            with st.spinner("Gerando PDF..."):
                pdf_bytes = gerar_pdf_medico(usuario_id)
            nome = f"relatorio_medtrack_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
            st.download_button(
                label="⬇️ Baixar relatório PDF",
                data=pdf_bytes,
                file_name=nome,
                mime="application/pdf",
                use_container_width=True,
            )

    st.divider()

    st.markdown("#### Histórico de links")
    links = listar_links_usuario(usuario_id)

    if not links:
        st.caption("Nenhum link gerado ainda.")
    else:
        for link in links:
            expirou  = str(link["expira_em"]) < str(datetime.now())
            status   = "❌ Expirado" if expirou else "✅ Ativo"
            acessado = (
                f"Acessado em {_fmt(link['acessado_em'])}"
                if link["acessado_em"] else "Não acessado"
            )
            st.markdown(
                f"`{_fmt(link['created_at'])}` &nbsp; {status} &nbsp;·&nbsp; "
                f"Expira: {_fmt(link['expira_em'])} &nbsp;·&nbsp; {acessado}",
                unsafe_allow_html=True
            )
