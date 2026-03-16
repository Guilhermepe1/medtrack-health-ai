"""
UI responsável pela timeline de exames.
"""

import streamlit as st

from repositories.exame_repository import montar_timeline_exames, excluir_exame


def render_timeline():

    st.subheader("Timeline de Saúde")

    tipos = ["Todos", "Hemograma", "Colesterol", "Diabetes", "Imagem", "Outros"]

    filtro = st.selectbox("Filtrar tipo de exame", tipos)

    usuario_id = st.session_state["usuario_id"]

    timeline = montar_timeline_exames(usuario_id)

    for categoria in timeline:

        if filtro != "Todos" and categoria != filtro:
            continue

        st.header(f"🧬 {categoria}")

        anos = timeline[categoria]

        for ano in anos:

            st.subheader(ano)

            exames = anos[ano]

            for exame in exames:

                with st.expander(f"📄 {exame.arquivo}"):

                    st.write(exame.resumo)

                    if st.button(f"Excluir exame {exame.id}"):

                        excluir_exame(exame.id)

                        st.success("Exame excluído com sucesso!")

                        st.rerun()