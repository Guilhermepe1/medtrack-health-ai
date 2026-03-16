"""
UI para visualização de valores laboratoriais extraídos dos exames.
"""

import streamlit as st
import pandas as pd

from repositories.valores_repository import (
    buscar_parametros_disponiveis,
    buscar_evolucao_parametro
)


STATUS_COR = {
    "alto":  "🔴",
    "baixo": "🔵",
    "normal": "🟢"
}


def render_valores():

    st.subheader("Valores Laboratoriais")

    usuario_id = st.session_state["usuario_id"]

    parametros = buscar_parametros_disponiveis(usuario_id)

    if not parametros:
        st.info("Nenhum valor extraído ainda. Faça upload de um exame para começar.")
        return

    # seletor de parâmetro
    parametro = st.selectbox("Selecione o parâmetro", parametros)

    if not parametro:
        return

    dados = buscar_evolucao_parametro(usuario_id, parametro)

    if not dados:
        st.warning("Nenhum dado encontrado para este parâmetro.")
        return

    # monta dataframe
    df = pd.DataFrame([{
        "Data":       str(row["data_coleta"]) if row["data_coleta"] else "—",
        "Valor":      row["valor"],
        "Unidade":    row["unidade"] or "—",
        "Ref. mín":   row["referencia_min"] if row["referencia_min"] is not None else "—",
        "Ref. máx":   row["referencia_max"] if row["referencia_max"] is not None else "—",
        "Status":     STATUS_COR.get(row["status"], "—") + " " + (row["status"] or "—"),
    } for row in dados])

    # tabela
    st.markdown("#### Histórico")
    st.dataframe(df, use_container_width=True, hide_index=True)

    # gráfico — só plota se tiver datas e valores numéricos
    df_grafico = pd.DataFrame([{
        "Data":  row["data_coleta"],
        "Valor": float(row["valor"]) if row["valor"] is not None else None,
        "Ref. mín": float(row["referencia_min"]) if row["referencia_min"] is not None else None,
        "Ref. máx": float(row["referencia_max"]) if row["referencia_max"] is not None else None,
    } for row in dados if row["data_coleta"] and row["valor"] is not None])

    if len(df_grafico) >= 1:
        st.markdown("#### Evolução ao longo do tempo")
        df_grafico = df_grafico.set_index("Data")

        # plota valor + linhas de referência
        colunas = ["Valor"]
        if df_grafico["Ref. mín"].notna().any():
            colunas.append("Ref. mín")
        if df_grafico["Ref. máx"].notna().any():
            colunas.append("Ref. máx")

        st.line_chart(df_grafico[colunas])
    else:
        st.info("Adicione mais exames para visualizar a evolução temporal.")
