"""
UI do dashboard de saúde personalizado.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date

from services.dashboard_service import (
    calcular_score_saude,
    calcular_imc,
    calcular_idade,
    gerar_recomendacoes,
    buscar_melhor_parametro_grafico,
)
from repositories.alertas_repository import buscar_todos_alertas
from repositories.exame_repository import listar_exames
from repositories.perfil_repository import buscar_perfil


def _formatar_data(data_str):
    try:
        return datetime.strptime(str(data_str)[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
    except Exception:
        return str(data_str)[:10]


def _dias_desde(data_str):
    try:
        d = datetime.strptime(str(data_str)[:10], "%Y-%m-%d").date()
        return (date.today() - d).days
    except Exception:
        return None


def render_score(score, categoria, cor):
    """Card principal do score de saúde."""
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {cor}22, {cor}11);
        border: 2px solid {cor}44;
        border-radius: 20px;
        padding: 1.8rem 2rem;
        text-align: center;
        margin-bottom: 1rem;
    ">
        <div style="font-size:11px;font-weight:600;letter-spacing:1.5px;
                    color:{cor};text-transform:uppercase;margin-bottom:8px">
            Score de Saúde
        </div>
        <div style="font-size:64px;font-weight:700;color:{cor};
                    line-height:1;margin-bottom:8px">
            {score}
        </div>
        <div style="font-size:16px;font-weight:500;color:{cor}CC">
            {categoria}
        </div>
        <div style="
            margin-top:16px;
            height:8px;
            background:{cor}22;
            border-radius:4px;
            overflow:hidden;
        ">
            <div style="
                width:{score}%;
                height:100%;
                background:linear-gradient(90deg,{cor}88,{cor});
                border-radius:4px;
                transition:width 0.5s ease;
            "></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_card_metrica(icone, label, valor, sub=None, cor="#2B7FD4"):
    sub_html = f'<div style="font-size:11px;color:#6B8CB0;margin-top:2px">{sub}</div>' if sub else ""
    st.markdown(f"""
    <div style="
        background:#FFFFFF;
        border:1px solid #E0EAF5;
        border-radius:14px;
        padding:1.1rem 1.2rem;
        height:100%;
    ">
        <div style="font-size:20px;margin-bottom:6px">{icone}</div>
        <div style="font-size:11px;font-weight:600;color:#6B8CB0;
                    text-transform:uppercase;letter-spacing:0.5px">
            {label}
        </div>
        <div style="font-size:22px;font-weight:700;color:{cor};margin-top:4px">
            {valor}
        </div>
        {sub_html}
    </div>
    """, unsafe_allow_html=True)


def render_dashboard():
    usuario_id = st.session_state["usuario_id"]

    # carrega dados
    with st.spinner("Carregando seu painel..."):
        score, categoria, cor = calcular_score_saude(usuario_id)
        perfil                = buscar_perfil(usuario_id)
        exames                = listar_exames(usuario_id)
        alertas               = buscar_todos_alertas(usuario_id)
        nao_lidos             = [a for a in alertas if not a["lido"]]
        recomendacoes         = gerar_recomendacoes(usuario_id)
        param_grafico, dados_grafico = buscar_melhor_parametro_grafico(usuario_id)

    # ── Linha 1: Score + Métricas ──
    col_score, col_metricas = st.columns([1, 2], gap="large")

    with col_score:
        render_score(score, categoria, cor)

    with col_metricas:
        # métricas do perfil
        imc_result = calcular_imc(perfil)
        idade      = calcular_idade(perfil)

        m1, m2 = st.columns(2)

        with m1:
            if imc_result:
                imc, cat_imc = imc_result
                cor_imc = "#00C9A7" if cat_imc == "Peso normal" else "#F5A623"
                render_card_metrica("⚖️", "IMC", imc, cat_imc, cor_imc)
            else:
                render_card_metrica("⚖️", "IMC", "—",
                                    "Complete seu perfil", "#6B8CB0")

        with m2:
            if idade:
                render_card_metrica("🎂", "Idade", f"{idade} anos",
                                    cor="#1A2A6C")
            else:
                render_card_metrica("🎂", "Idade", "—",
                                    "Complete seu perfil", "#6B8CB0")

        m3, m4 = st.columns(2)

        with m3:
            cor_alertas = "#E84545" if nao_lidos else "#00C9A7"
            render_card_metrica(
                "⚠️" if nao_lidos else "✅",
                "Alertas ativos",
                str(len(nao_lidos)),
                "não lidos" if nao_lidos else "tudo ok",
                cor_alertas
            )

        with m4:
            total_exames = len(exames)
            render_card_metrica("📋", "Total de exames",
                                 str(total_exames),
                                 "cadastrados", "#2B7FD4")

    st.divider()

    # ── Linha 2: Último exame + Gráfico ──
    col_ultimo, col_grafico = st.columns([1, 2], gap="large")

    with col_ultimo:
        st.markdown("#### 📄 Último exame")

        if exames:
            ultimo     = exames[0]
            nome       = getattr(ultimo, "nome_exame", None) or ultimo.arquivo
            data_ref   = getattr(ultimo, "data_exame", None) or ultimo.data_upload[:10]
            dias       = _dias_desde(data_ref)
            data_fmt   = _formatar_data(data_ref)
            dias_label = f"há {dias} dias" if dias is not None else ""

            st.markdown(f"""
            <div style="
                background:#FFFFFF;
                border:1px solid #E0EAF5;
                border-left:4px solid #2B7FD4;
                border-radius:0 14px 14px 0;
                padding:1rem 1.2rem;
            ">
                <div style="font-size:14px;font-weight:600;
                            color:#1A2A6C;margin-bottom:4px">
                    {nome}
                </div>
                <div style="font-size:12px;color:#6B8CB0">
                    📅 {data_fmt} &nbsp;·&nbsp; {dias_label}
                </div>
                {"<div style='font-size:12px;color:#6B8CB0;margin-top:2px'>👨‍⚕️ " + ultimo.medico + "</div>" if getattr(ultimo, "medico", None) else ""}
            </div>
            """, unsafe_allow_html=True)

            if len(exames) > 1:
                st.caption(f"E mais {len(exames) - 1} exame(s) no histórico.")
        else:
            st.info("Nenhum exame cadastrado ainda.")
            if st.button("📤 Enviar primeiro exame", use_container_width=True):
                st.session_state["pagina"] = "upload"
                st.rerun()

    with col_grafico:
        st.markdown(f"#### 📊 Evolução{': ' + param_grafico if param_grafico else ''}")

        if param_grafico and dados_grafico:
            df = pd.DataFrame([{
                "Data":  d["data_coleta"],
                "Valor": float(d["valor"]),
                "Ref. mín": float(d["referencia_min"]) if d.get("referencia_min") else None,
                "Ref. máx": float(d.get("referencia_max")) if d.get("referencia_max") else None,
            } for d in dados_grafico]).set_index("Data")

            colunas = ["Valor"]
            if df["Ref. mín"].notna().any():
                colunas.append("Ref. mín")
            if df["Ref. máx"].notna().any():
                colunas.append("Ref. máx")

            st.line_chart(df[colunas], height=180)
            unidade = dados_grafico[0].get("unidade") or ""
            st.caption(f"Unidade: {unidade}" if unidade else "")
        else:
            st.info(
                "Faça upload de exames com valores laboratoriais "
                "para ver a evolução aqui."
            )

    st.divider()

    # ── Linha 3: Recomendações ──
    st.markdown("#### 💡 Recomendações personalizadas")

    if recomendacoes:
        for rec in recomendacoes:
            prioridade_cor = {1: "#E84545", 2: "#F5A623",
                              3: "#2B7FD4", 4: "#6B8CB0"}
            cor_rec = prioridade_cor.get(rec["prioridade"], "#6B8CB0")

            st.markdown(f"""
            <div style="
                background:#FFFFFF;
                border:1px solid #E0EAF5;
                border-left:3px solid {cor_rec};
                border-radius:0 10px 10px 0;
                padding:0.8rem 1rem;
                margin-bottom:8px;
                font-size:13px;
                color:#1A2A6C;
            ">
                {rec['icone']} &nbsp; {rec['texto']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ Tudo em ordem! Continue mantendo seus exames atualizados.")

    st.divider()

    # ── Alertas ativos ──
    if nao_lidos:
        st.markdown("#### ⚠️ Alertas clínicos não lidos")

        STATUS_COR = {"alto": "#E84545", "baixo": "#2B7FD4"}

        for alerta in nao_lidos[:5]:
            cor_alerta = STATUS_COR.get(alerta["status"], "#888")
            st.markdown(f"""
            <div style="
                background:#FFFFFF;
                border-left:4px solid {cor_alerta};
                border-radius:0 10px 10px 0;
                border-top:1px solid {cor_alerta}22;
                border-right:1px solid {cor_alerta}22;
                border-bottom:1px solid {cor_alerta}22;
                padding:0.8rem 1rem;
                margin-bottom:6px;
                font-size:13px;
            ">
                <strong style="color:{cor_alerta}">{alerta['parametro']}</strong>
                &nbsp;—&nbsp;
                <span style="color:#1A2A6C">
                    {alerta['valor']} {alerta.get('unidade') or ''}
                    ({alerta['status'].upper()})
                </span>
                <span style="color:#6B8CB0;font-size:11px;margin-left:8px">
                    {alerta.get('arquivo','')}
                </span>
            </div>
            """, unsafe_allow_html=True)

        if len(nao_lidos) > 5:
            st.caption(f"E mais {len(nao_lidos) - 5} alerta(s)...")

        if st.button("Ver todos os alertas →", type="secondary"):
            st.session_state["pagina"] = "alertas"
            st.rerun()
