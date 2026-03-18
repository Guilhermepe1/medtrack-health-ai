"""
UI de Minha Conta — visualização e edição de dados cadastrais.
"""

import re
import requests
import streamlit as st
import bcrypt

from repositories.usuario_repository import (
    buscar_dados_completos,
    buscar_usuario_por_username,
    buscar_usuario_por_cpf,
    buscar_usuario_por_email,
    atualizar_dados_usuario,
    get_connection,
    get_cursor,
)


# ── Helpers ──

def _limpar(valor, apenas_numeros=False):
    if not valor:
        return ""
    if apenas_numeros:
        return re.sub(r"\D", "", valor)
    return str(valor).strip()


def _formatar_cpf(cpf):
    c = re.sub(r"\D", "", cpf)
    return f"{c[:3]}.{c[3:6]}.{c[6:9]}-{c[9:]}" if len(c) == 11 else cpf


def _formatar_celular(cel):
    c = re.sub(r"\D", "", cel)
    if len(c) == 11:
        return f"({c[:2]}) {c[2:7]}-{c[7:]}"
    if len(c) == 10:
        return f"({c[:2]}) {c[2:6]}-{c[6:]}"
    return cel


def _validar_cpf(cpf):
    c = re.sub(r"\D", "", cpf)
    if len(c) != 11 or len(set(c)) == 1:
        return False
    for i in range(9, 11):
        soma = sum(int(c[j]) * (i + 1 - j) for j in range(i))
        if (soma * 10 % 11) % 10 != int(c[i]):
            return False
    return True


def _validar_email(email):
    return bool(re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-z]{2,}$", email, re.I))


def _validar_celular(cel):
    c = re.sub(r"\D", "", cel)
    return len(c) in (10, 11) and len(set(c)) > 1


def _buscar_cep(cep):
    cep_limpo = re.sub(r"\D", "", cep)
    if len(cep_limpo) != 8:
        return None
    try:
        resp = requests.get(
            f"https://viacep.com.br/ws/{cep_limpo}/json/", timeout=5
        )
        data = resp.json()
        if "erro" not in data:
            return data
    except Exception:
        pass
    return None


def _alterar_senha(usuario_id, senha_atual, nova_senha, confirma):
    """Valida e atualiza a senha do usuário."""
    conn = get_connection()
    cursor = get_cursor(conn)

    cursor.execute(
        "SELECT senha FROM usuarios WHERE id = %s", (usuario_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row or not row["senha"]:
        return False, "Conta criada via Google não possui senha cadastrada."

    if not bcrypt.checkpw(senha_atual.encode(), row["senha"].encode()):
        return False, "Senha atual incorreta."

    if len(nova_senha) < 8:
        return False, "A nova senha deve ter pelo menos 8 caracteres."

    if nova_senha != confirma:
        return False, "As senhas não coincidem."

    nova_hash = bcrypt.hashpw(nova_senha.encode(), bcrypt.gensalt()).decode()

    conn = get_connection()
    cursor = get_cursor(conn)
    cursor.execute(
        "UPDATE usuarios SET senha = %s WHERE id = %s",
        (nova_hash, usuario_id)
    )
    conn.commit()
    conn.close()

    return True, "Senha alterada com sucesso!"


# ── UI principal ──

def render_minha_conta():
    usuario_id = st.session_state["usuario_id"]
    dados      = buscar_dados_completos(usuario_id)

    if not dados:
        st.error("Não foi possível carregar seus dados.")
        return

    tab_dados, tab_endereco, tab_senha = st.tabs([
        "👤 Dados pessoais",
        "📍 Endereço",
        "🔑 Alterar senha",
    ])

    # ── Tab Dados pessoais ──
    with tab_dados:
        st.markdown("#### Informações de identificação e contato")
        st.caption("Campos marcados com * são obrigatórios.")

        with st.form("form_dados_pessoais"):
            col1, col2 = st.columns(2)

            with col1:
                nome_completo = st.text_input(
                    "Nome completo *",
                    value=dados.get("nome_completo") or ""
                )
                email = st.text_input(
                    "E-mail *",
                    value=dados.get("email") or ""
                )
                cpf = st.text_input(
                    "CPF *",
                    value=dados.get("cpf") or "",
                    disabled=True,
                    help="O CPF não pode ser alterado após o cadastro."
                )

            with col2:
                from datetime import date as _date
                nasc_atual = dados.get("data_nascimento")
                data_nasc  = st.date_input(
                    "Data de nascimento *",
                    value=nasc_atual or None,
                    format="DD/MM/YYYY"
                )
                celular = st.text_input(
                    "Celular *",
                    value=dados.get("celular") or "",
                    placeholder="(11) 99999-9999",
                    max_chars=15
                )

            salvar_dados = st.form_submit_button(
                "💾 Salvar dados pessoais", use_container_width=True
            )

        if salvar_dados:
            erros = []

            if not nome_completo.strip():
                erros.append("Nome completo é obrigatório.")

            if not _validar_email(email):
                erros.append("E-mail inválido.")
            else:
                existente = buscar_usuario_por_email(email)
                if existente and existente["id"] != usuario_id:
                    erros.append("Este e-mail já está sendo usado por outra conta.")

            if not data_nasc:
                erros.append("Data de nascimento é obrigatória.")

            if not _validar_celular(celular):
                erros.append(
                    "Celular inválido. Informe um número real com DDD, "
                    "ex: (11) 99999-9999."
                )

            if erros:
                for e in erros:
                    st.error(e)
            else:
                atualizar_dados_usuario(usuario_id, {
                    **{k: dados.get(k) for k in [
                        "cep", "logradouro", "numero", "complemento",
                        "bairro", "cidade", "estado"
                    ]},
                    "nome_completo":  nome_completo.strip(),
                    "data_nascimento": str(data_nasc),
                    "cpf":            dados.get("cpf"),
                    "email":          email.strip().lower(),
                    "celular":        _formatar_celular(celular),
                })
                st.success("✅ Dados pessoais atualizados com sucesso!")
                st.rerun()

    # ── Tab Endereço ──
    with tab_endereco:
        st.markdown("#### Endereço residencial")

        col_cep, col_btn = st.columns([2, 1])
        with col_cep:
            cep_input = st.text_input(
                "CEP *",
                value=dados.get("cep") or "",
                max_chars=9,
                placeholder="00000-000"
            )
        with col_btn:
            st.markdown("<div style='margin-top:28px'>", unsafe_allow_html=True)
            if st.button("🔍 Buscar CEP", use_container_width=True):
                with st.spinner("Buscando..."):
                    resultado = _buscar_cep(cep_input)
                if resultado:
                    st.session_state["edit_logradouro"] = resultado.get("logradouro", "")
                    st.session_state["edit_bairro"]     = resultado.get("bairro", "")
                    st.session_state["edit_cidade"]     = resultado.get("localidade", "")
                    st.session_state["edit_estado"]     = resultado.get("uf", "")
                    st.success("Endereço encontrado!")
                else:
                    st.warning("CEP não encontrado. Preencha manualmente.")
            st.markdown("</div>", unsafe_allow_html=True)

        with st.form("form_endereco"):
            col3, col4 = st.columns([3, 1])
            with col3:
                logradouro = st.text_input(
                    "Logradouro *",
                    value=st.session_state.get(
                        "edit_logradouro", dados.get("logradouro") or ""
                    )
                )
            with col4:
                numero = st.text_input(
                    "Número *",
                    value=dados.get("numero") or ""
                )

            col5, col6 = st.columns(2)
            with col5:
                complemento = st.text_input(
                    "Complemento",
                    value=dados.get("complemento") or ""
                )
            with col6:
                bairro = st.text_input(
                    "Bairro *",
                    value=st.session_state.get(
                        "edit_bairro", dados.get("bairro") or ""
                    )
                )

            col7, col8 = st.columns([3, 1])
            with col7:
                cidade = st.text_input(
                    "Cidade *",
                    value=st.session_state.get(
                        "edit_cidade", dados.get("cidade") or ""
                    )
                )
            with col8:
                estados = [
                    "", "AC","AL","AP","AM","BA","CE","DF","ES","GO",
                    "MA","MT","MS","MG","PA","PB","PR","PE","PI","RJ",
                    "RN","RS","RO","RR","SC","SP","SE","TO"
                ]
                estado_atual = st.session_state.get(
                    "edit_estado", dados.get("estado") or ""
                )
                estado_idx = estados.index(estado_atual) \
                    if estado_atual in estados else 0
                estado = st.selectbox("Estado *", estados, index=estado_idx)

            salvar_end = st.form_submit_button(
                "💾 Salvar endereço", use_container_width=True
            )

        if salvar_end:
            erros = []

            cep_limpo = re.sub(r"\D", "", cep_input)
            if len(cep_limpo) != 8:
                erros.append("CEP inválido. Deve ter 8 dígitos.")
            if not logradouro.strip():
                erros.append("Logradouro é obrigatório.")
            if not numero.strip():
                erros.append("Número é obrigatório.")
            if not bairro.strip():
                erros.append("Bairro é obrigatório.")
            if not cidade.strip():
                erros.append("Cidade é obrigatória.")
            if not estado:
                erros.append("Estado é obrigatório.")

            if erros:
                for e in erros:
                    st.error(e)
            else:
                atualizar_dados_usuario(usuario_id, {
                    **{k: dados.get(k) for k in [
                        "nome_completo", "data_nascimento", "cpf",
                        "email", "celular"
                    ]},
                    "cep":         cep_limpo,
                    "logradouro":  logradouro.strip(),
                    "numero":      numero.strip(),
                    "complemento": complemento.strip() or None,
                    "bairro":      bairro.strip(),
                    "cidade":      cidade.strip(),
                    "estado":      estado,
                })

                for key in ["edit_logradouro", "edit_bairro",
                            "edit_cidade", "edit_estado"]:
                    st.session_state.pop(key, None)

                st.success("✅ Endereço atualizado com sucesso!")
                st.rerun()

    # ── Tab Alterar senha ──
    with tab_senha:
        st.markdown("#### Alterar senha")

        with st.form("form_senha"):
            senha_atual   = st.text_input("Senha atual *", type="password")
            nova_senha    = st.text_input(
                "Nova senha *", type="password",
                placeholder="mínimo 8 caracteres"
            )
            confirma_nova = st.text_input("Confirmar nova senha *", type="password")

            alterar = st.form_submit_button(
                "🔑 Alterar senha", use_container_width=True
            )

        if alterar:
            if not senha_atual:
                st.error("Informe sua senha atual.")
            elif not nova_senha:
                st.error("Informe a nova senha.")
            elif not confirma_nova:
                st.error("Confirme a nova senha.")
            else:
                sucesso, msg = _alterar_senha(
                    usuario_id, senha_atual, nova_senha, confirma_nova
                )
                if sucesso:
                    st.success(msg)
                else:
                    st.error(msg)