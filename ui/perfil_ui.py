"""
UI do perfil de saúde — modal acionado pelo avatar na sidebar.
"""

import streamlit as st
from datetime import date

from repositories.perfil_repository import buscar_perfil, salvar_perfil


CONDICOES_OPCOES = [
    "Diabetes tipo 1",
    "Diabetes tipo 2",
    "Hipertensão",
    "Hipotensão",
    "Hipotireoidismo",
    "Hipertireoidismo",
    "Colesterol alto",
    "Doença cardiovascular",
    "Asma",
    "Anemia",
    "Obesidade",
    "Depressão / Ansiedade",
    "Doença renal crônica",
]


def render_avatar_sidebar(nome):
    """
    Renderiza o avatar do usuário na sidebar com botão que abre o perfil.
    Substitui a função sidebar_usuario do theme.py.
    """
    inicial = nome[0].upper() if nome else "?"

    st.sidebar.markdown(f"""
    <div style="
        display:flex; align-items:center; gap:10px;
        padding:0.7rem 1rem;
        background:rgba(255,255,255,0.08);
        border-radius:12px;
        margin:0 1rem 0.5rem 1rem;
    ">
        <div style="
            width:36px; height:36px;
            background:linear-gradient(135deg,#00C9A7,#2B7FD4);
            border-radius:50%;
            display:flex; align-items:center; justify-content:center;
            color:white; font-weight:600; font-size:15px; flex-shrink:0;
        ">{inicial}</div>
        <div>
            <div style="font-size:13px;font-weight:500;color:#fff;">{nome}</div>
            <div style="font-size:11px;color:rgba(255,255,255,0.5);">Paciente</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.sidebar.button("👤  Meu Perfil de Saúde",
                         use_container_width=True,
                         key="btn_perfil"):
        st.session_state["modal_perfil"] = True


def render_modal_perfil():
    """
    Renderiza o modal de perfil de saúde quando ativado.
    """
    if not st.session_state.get("modal_perfil"):
        return

    usuario_id = st.session_state["usuario_id"]
    perfil     = buscar_perfil(usuario_id) or {}

    with st.container(border=True):

        col_titulo, col_fechar = st.columns([5, 1])
        with col_titulo:
            st.markdown("### 👤 Perfil de Saúde")
            st.caption("Essas informações ajudam a IA a personalizar as respostas sobre seus exames.")
        with col_fechar:
            if st.button("✕", key="fechar_perfil", type="secondary"):
                st.session_state["modal_perfil"] = False
                st.rerun()

        st.divider()

        # ── Dados básicos ──
        st.markdown("**Dados básicos**")
        col1, col2 = st.columns(2)

        with col1:
            data_nasc = st.date_input(
                "Data de nascimento",
                value=perfil.get("data_nascimento") or None,
                format="DD/MM/YYYY",
                min_value=date(1920, 1, 1),
                max_value=date.today()
            )
            peso = st.number_input(
                "Peso (kg)",
                min_value=0.0,
                max_value=300.0,
                value=float(perfil["peso"]) if perfil.get("peso") else 0.0,
                step=0.5,
                format="%.1f"
            )

        with col2:
            sexo = st.selectbox(
                "Sexo biológico",
                ["", "Masculino", "Feminino", "Outro"],
                index=["", "Masculino", "Feminino", "Outro"].index(
                    perfil.get("sexo") or ""
                )
            )
            altura = st.number_input(
                "Altura (cm)",
                min_value=0,
                max_value=250,
                value=int(perfil["altura"]) if perfil.get("altura") else 0,
                step=1
            )

        # IMC em tempo real
        if peso > 0 and altura > 0:
            imc = round(peso / ((altura / 100) ** 2), 1)
            if imc < 18.5:
                cat = "Abaixo do peso"
            elif imc < 25:
                cat = "Peso normal ✅"
            elif imc < 30:
                cat = "Sobrepeso"
            else:
                cat = "Obesidade"
            st.info(f"IMC calculado: **{imc}** — {cat}")

        st.divider()

        # ── Condições de saúde ──
        st.markdown("**Condições de saúde**")

        condicoes_atuais = list(perfil.get("condicoes") or [])
        condicoes_sel = st.multiselect(
            "Selecione as condições que se aplicam",
            options=CONDICOES_OPCOES,
            default=[c for c in condicoes_atuais if c in CONDICOES_OPCOES]
        )

        outras = st.text_input(
            "Outras condições (separe por vírgula)",
            value=perfil.get("outras_condicoes") or "",
            placeholder="Ex: lúpus, fibromialgia"
        )

        st.divider()

        # ── Medicamentos ──
        st.markdown("**Medicamentos em uso**")
        medicamentos = st.text_area(
            "Liste os medicamentos que usa regularmente",
            value=perfil.get("medicamentos") or "",
            placeholder="Ex: Metformina 500mg, Losartana 50mg, Vitamina D 2000UI",
            height=90
        )

        st.divider()

        # ── Hábitos ──
        st.markdown("**Hábitos de vida**")
        col3, col4, col5 = st.columns(3)

        with col3:
            fumante = st.selectbox(
                "Tabagismo",
                ["Não", "Ex-fumante", "Sim (leve)", "Sim (moderado)", "Sim (intenso)"],
                index=["Não", "Ex-fumante", "Sim (leve)", "Sim (moderado)", "Sim (intenso)"].index(
                    perfil.get("fumante") or "Não"
                )
            )

        with col4:
            alcool = st.selectbox(
                "Consumo de álcool",
                ["Não consome", "Ocasional", "Moderado", "Frequente"],
                index=["Não consome", "Ocasional", "Moderado", "Frequente"].index(
                    perfil.get("consumo_alcool") or "Não consome"
                )
            )

        with col5:
            atividade = st.selectbox(
                "Atividade física",
                ["Sedentário", "Leve (1-2x/sem)", "Moderado (3-4x/sem)", "Intenso (5+/sem)"],
                index=["Sedentário", "Leve (1-2x/sem)", "Moderado (3-4x/sem)", "Intenso (5+/sem)"].index(
                    perfil.get("atividade_fisica") or "Sedentário"
                )
            )

        st.divider()

        if st.button("💾 Salvar perfil", use_container_width=True):
            salvar_perfil(usuario_id, {
                "data_nascimento":  str(data_nasc) if data_nasc else None,
                "sexo":             sexo or None,
                "peso":             peso if peso > 0 else None,
                "altura":           altura if altura > 0 else None,
                "condicoes":        condicoes_sel,
                "outras_condicoes": outras or None,
                "medicamentos":     medicamentos or None,
                "fumante":          fumante,
                "consumo_alcool":   alcool,
                "atividade_fisica": atividade,
            })
            st.success("✅ Perfil salvo com sucesso!")
            st.session_state["modal_perfil"] = False
            st.rerun()