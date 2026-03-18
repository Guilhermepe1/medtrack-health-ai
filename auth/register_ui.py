"""
UI de cadastro completo de usuário.
Coleta dados de identificação, contato e endereço.
"""

import re
import requests
import streamlit as st
import bcrypt

from repositories.usuario_repository import (
    buscar_usuario_por_username,
    buscar_usuario_por_cpf,
    buscar_usuario_por_email,
    criar_usuario,
)


# ── Validações ──

def _validar_cpf(cpf):
    """Valida CPF com algoritmo oficial."""
    cpf = re.sub(r"\D", "", cpf)
    if len(cpf) != 11 or len(set(cpf)) == 1:
        return False
    for i in range(9, 11):
        soma = sum(int(cpf[j]) * (i + 1 - j) for j in range(i))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True


def _formatar_cpf(cpf):
    cpf = re.sub(r"\D", "", cpf)
    if len(cpf) == 11:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    return cpf


def _formatar_celular(cel):
    cel = re.sub(r"\D", "", cel)
    if len(cel) == 11:
        return f"({cel[:2]}) {cel[2:7]}-{cel[7:]}"
    elif len(cel) == 10:
        return f"({cel[:2]}) {cel[2:6]}-{cel[6:]}"
    return cel


def _buscar_cep(cep):
    """Consulta ViaCEP e retorna dados do endereço."""
    cep_limpo = re.sub(r"\D", "", cep)
    if len(cep_limpo) != 8:
        return None
    try:
        resp = requests.get(
            f"https://viacep.com.br/ws/{cep_limpo}/json/",
            timeout=5
        )
        data = resp.json()
        if "erro" not in data:
            return data
    except Exception:
        pass
    return None


def render_registro():
    st.title("Criar conta")
    st.caption("Todos os campos marcados com * são obrigatórios.")

    # ── Dados de acesso ──
    st.markdown("#### 🔑 Dados de acesso")

    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("Username *", placeholder="como_quer_ser_chamado")
    with col2:
        senha = st.text_input("Senha *", type="password", placeholder="mínimo 8 caracteres")

    confirma_senha = st.text_input("Confirmar senha *", type="password")

    st.divider()

    # ── Identificação pessoal ──
    st.markdown("#### 👤 Identificação")

    nome_completo = st.text_input("Nome completo *", placeholder="Como aparece no documento")

    col3, col4 = st.columns(2)
    with col3:
        data_nasc = st.date_input(
            "Data de nascimento *",
            value=None,
            format="DD/MM/YYYY",
            min_value=None,
            max_value=None
        )
    with col4:
        cpf_input = st.text_input("CPF *", placeholder="000.000.000-00", max_chars=14)

    st.divider()

    # ── Contato ──
    st.markdown("#### 📞 Contato")

    col5, col6 = st.columns(2)
    with col5:
        email = st.text_input("E-mail *", placeholder="seu@email.com")
    with col6:
        celular = st.text_input("Celular *", placeholder="(11) 99999-9999", max_chars=15)

    st.divider()

    # ── Endereço com busca automática por CEP ──
    st.markdown("#### 📍 Endereço")

    col_cep, col_btn = st.columns([2, 1])
    with col_cep:
        cep_input = st.text_input("CEP *", placeholder="00000-000", max_chars=9)
    with col_btn:
        st.markdown("<div style='margin-top:28px'>", unsafe_allow_html=True)
        buscar_cep = st.button("🔍 Buscar CEP", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # busca automática ao clicar
    if buscar_cep and cep_input:
        with st.spinner("Buscando endereço..."):
            dados_cep = _buscar_cep(cep_input)
        if dados_cep:
            st.session_state["cep_logradouro"] = dados_cep.get("logradouro", "")
            st.session_state["cep_bairro"]     = dados_cep.get("bairro", "")
            st.session_state["cep_cidade"]     = dados_cep.get("localidade", "")
            st.session_state["cep_estado"]     = dados_cep.get("uf", "")
            st.success("Endereço encontrado!")
        else:
            st.warning("CEP não encontrado. Preencha manualmente.")

    col7, col8 = st.columns([3, 1])
    with col7:
        logradouro = st.text_input(
            "Logradouro *",
            value=st.session_state.get("cep_logradouro", ""),
            placeholder="Rua, Avenida, etc."
        )
    with col8:
        numero = st.text_input("Número *", placeholder="123")

    col9, col10 = st.columns(2)
    with col9:
        complemento = st.text_input("Complemento", placeholder="Apto, Bloco, etc.")
    with col10:
        bairro = st.text_input(
            "Bairro *",
            value=st.session_state.get("cep_bairro", "")
        )

    col11, col12 = st.columns([3, 1])
    with col11:
        cidade = st.text_input(
            "Cidade *",
            value=st.session_state.get("cep_cidade", "")
        )
    with col12:
        estados = [
            "", "AC","AL","AP","AM","BA","CE","DF","ES","GO",
            "MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ",
            "RN","RS","RO","RR","SC","SP","SE","TO"
        ]
        estado_atual = st.session_state.get("cep_estado", "")
        estado_idx   = estados.index(estado_atual) if estado_atual in estados else 0
        estado = st.selectbox("Estado *", estados, index=estado_idx)

    st.divider()

    # ── Botão de cadastro ──
    if st.button("✅ Criar conta", use_container_width=True):

        erros = []

        # validações
        if not username:
            erros.append("Username é obrigatório.")
        elif buscar_usuario_por_username(username):
            erros.append("Este username já está em uso.")

        if not senha or len(senha) < 8:
            erros.append("A senha deve ter pelo menos 8 caracteres.")

        if senha != confirma_senha:
            erros.append("As senhas não coincidem.")

        if not nome_completo:
            erros.append("Nome completo é obrigatório.")

        if not data_nasc:
            erros.append("Data de nascimento é obrigatória.")

        cpf_limpo = re.sub(r"\D", "", cpf_input)
        if not _validar_cpf(cpf_limpo):
            erros.append("CPF inválido.")
        elif buscar_usuario_por_cpf(_formatar_cpf(cpf_limpo)):
            erros.append("CPF já cadastrado.")

        if not email or "@" not in email:
            erros.append("E-mail inválido.")
        elif buscar_usuario_por_email(email):
            erros.append("E-mail já cadastrado.")

        cel_limpo = re.sub(r"\D", "", celular)
        if len(cel_limpo) < 10:
            erros.append("Celular inválido.")

        if not logradouro:
            erros.append("Logradouro é obrigatório.")
        if not numero:
            erros.append("Número é obrigatório.")
        if not bairro:
            erros.append("Bairro é obrigatório.")
        if not cidade:
            erros.append("Cidade é obrigatória.")
        if not estado:
            erros.append("Estado é obrigatório.")

        if erros:
            for erro in erros:
                st.error(erro)
            return

        # cria usuário
        senha_hash = bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()

        criar_usuario(
            nome=username,
            username=username,
            senha=senha_hash,
            dados_completos={
                "nome_completo":   nome_completo,
                "data_nascimento": str(data_nasc),
                "cpf":             _formatar_cpf(cpf_limpo),
                "email":           email,
                "celular":         _formatar_celular(cel_limpo),
                "cep":             re.sub(r"\D", "", cep_input),
                "logradouro":      logradouro,
                "numero":          numero,
                "complemento":     complemento or None,
                "bairro":          bairro,
                "cidade":          cidade,
                "estado":          estado,
            }
        )

        # limpa cache de CEP
        for key in ["cep_logradouro", "cep_bairro", "cep_cidade", "cep_estado"]:
            st.session_state.pop(key, None)

        st.success("✅ Conta criada com sucesso! Faça login para continuar.")