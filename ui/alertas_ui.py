"""
UI responsável pela exibição de alertas clínicos.
"""

import streamlit as st
from repositories.alertas_repository import (
    buscar_alertas_nao_lidos,
    buscar_todos_alertas,
    marcar_alerta_lido,
    marcar_todos_lidos
)

STATUS_CONFIG = {
    "alto":  {"icone": "🔴", "label": "Alto",  "cor": "error"},
    "baixo": {"icone": "🔵", "label": "Baixo", "cor": "info"},
}


def render_badge_alertas():
    """
    Exibe badge com contador de alertas não lidos.
    Chame essa função no topo do app, visível em todas as telas.
    """
    usuario_id = st.session_state.get("usuario_id")
    if not usuario_id:
        return

    nao_lidos = buscar_alertas_nao_lidos(usuario_id)

    if nao_lidos:
        st.warning(
            f"⚠️ Você tem **{len(nao_lidos)}** alerta(s) clínico(s) não lido(s).",
            icon="⚠️"
        )


def render_alertas():
    """
    Tela completa de alertas clínicos.
    """
    st.subheader("Alertas Clínicos")

    usuario_id = st.session_state["usuario_id"]
    alertas = buscar_todos_alertas(usuario_id)

    if not alertas:
        st.success("Nenhum alerta clínico encontrado. Seus valores estão dentro da referência!")
        return

    nao_lidos = [a for a in alertas if not a["lido"]]

    if nao_lidos:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{len(nao_lidos)}** alerta(s) não lido(s)")
        with col2:
            if st.button("Marcar todos como lidos"):
                marcar_todos_lidos(usuario_id)
                st.rerun()

    st.divider()

    for alerta in alertas:
        config = STATUS_CONFIG.get(alerta["status"], {"icone": "⚪", "label": alerta["status"], "cor": "info"})

        # card do alerta
        with st.container(border=True):
            col1, col2 = st.columns([5, 1])

            with col1:
                lido_label = "" if alerta["lido"] else " 🆕"
                st.markdown(
                    f"{config['icone']} **{alerta['parametro']}**{lido_label} — "
                    f"valor: **{alerta['valor']} {alerta['unidade'] or ''}**"
                )

                ref_min = alerta["referencia_min"]
                ref_max = alerta["referencia_max"]

                if ref_min is not None and ref_max is not None:
                    st.caption(f"Referência: {ref_min} – {ref_max} {alerta['unidade'] or ''}")
                elif ref_max is not None:
                    st.caption(f"Referência máxima: {ref_max} {alerta['unidade'] or ''}")
                elif ref_min is not None:
                    st.caption(f"Referência mínima: {ref_min} {alerta['unidade'] or ''}")

                data = str(alerta["created_at"])[:10]
                st.caption(f"Exame: {alerta['arquivo']} · Detectado em: {data}")

            with col2:
                if not alerta["lido"]:
                    if st.button("Lido", key=f"lido_{alerta['id']}"):
                        marcar_alerta_lido(alerta["id"])
                        st.rerun()
                else:
                    st.caption("✓ lido")