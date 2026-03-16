"""
UI responsável pela timeline de exames.
"""

import streamlit as st
from datetime import datetime

from repositories.exame_repository import montar_timeline_exames, excluir_exame


def _formatar_data(data_str):
    try:
        return datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return data_str


def render_timeline():

    tipos  = ["Todos", "Hemograma", "Colesterol", "Diabetes", "Imagem", "Outros"]
    filtro = st.selectbox("Filtrar tipo de exame", tipos)

    usuario_id = st.session_state["usuario_id"]
    timeline   = montar_timeline_exames(usuario_id)

    if not timeline:
        st.info("Nenhum exame encontrado. Faça upload do seu primeiro exame!")
        return

    for categoria in timeline:

        if filtro != "Todos" and categoria != filtro:
            continue

        st.markdown(f"### 🧬 {categoria}")

        anos = timeline[categoria]

        for ano in sorted(anos.keys(), reverse=True):

            st.markdown(f"**{ano}**")

            for exame in anos[ano]:

                titulo      = exame.nome_exame or exame.arquivo
                data_exibir = _formatar_data(exame.data_exame or exame.data_upload[:10])

                # linha de metadados
                info_parts = [f"📅 {data_exibir}"]
                if exame.medico:
                    info_parts.append(f"👨‍⚕️ {exame.medico}")
                if exame.hospital:
                    info_parts.append(f"🏥 {exame.hospital}")

                with st.expander(f"📄 {titulo}  —  {data_exibir}"):

                    st.caption("  ·  ".join(info_parts))
                    st.divider()
                    st.write(exame.resumo)

                    if st.button(
                        "🗑️ Excluir",
                        key=f"excluir_{exame.id}",
                        type="secondary"
                    ):
                        excluir_exame(exame.id)
                        st.success("Exame excluído!")
                        st.rerun()