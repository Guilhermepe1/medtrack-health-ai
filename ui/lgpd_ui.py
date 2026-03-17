"""
UI de conformidade LGPD:
- Termo de consentimento (bloqueia acesso até aceitar)
- Política de privacidade
- Logs de acesso
- Direito ao esquecimento
"""

import streamlit as st
from datetime import datetime

from repositories.lgpd_repository import (
    usuario_consentiu,
    registrar_consentimento,
    buscar_logs,
    excluir_todos_dados_usuario,
    VERSAO_ATUAL,
)

TERMO_TEXTO = """
**MedTrack Health AI — Termo de Consentimento e Política de Privacidade**
*Versão {versao} — Vigência: março de 2025*

---

**1. Quem somos**
O MedTrack Health AI é uma plataforma de centralização e interpretação de exames médicos e odontológicos com auxílio de inteligência artificial. Não somos um serviço médico — nossas respostas têm caráter informativo e não substituem consulta profissional.

**2. Quais dados coletamos**
Coletamos os seguintes dados pessoais e de saúde:
- Dados de identificação: nome, username, e-mail
- Dados de saúde: exames médicos, exames odontológicos, perfil de saúde (peso, altura, condições, medicamentos, hábitos)
- Dados de uso: logs de acesso, interações com o sistema

**3. Por que coletamos**
Seus dados são utilizados exclusivamente para:
- Prestar o serviço de interpretação e organização de exames
- Personalizar as respostas da inteligência artificial
- Garantir a segurança e integridade da sua conta

**4. Com quem compartilhamos**
Seus dados **nunca são vendidos** a terceiros. Utilizamos os seguintes serviços para operação da plataforma:
- **Supabase** (banco de dados em nuvem) — armazenamento seguro
- **Groq** (IA) — processamento de texto dos exames para geração de resumos
- **Streamlit Cloud** (hospedagem) — infraestrutura do app

Os textos dos seus exames são enviados à API da Groq para geração de resumos e respostas. Não armazenamos esses dados fora do nosso banco.

**5. Por quanto tempo guardamos**
Mantemos seus dados enquanto sua conta estiver ativa. Você pode solicitar a exclusão completa a qualquer momento pelo painel de privacidade.

**6. Seus direitos (LGPD — Lei 13.709/2018)**
Você tem direito a:
- **Acesso**: visualizar todos os dados que temos sobre você
- **Correção**: editar dados incorretos pelo perfil
- **Exclusão**: remover todos os seus dados permanentemente
- **Portabilidade**: exportar seus dados (em breve)
- **Revogação**: retirar o consentimento a qualquer momento

**7. Segurança**
Utilizamos criptografia de senhas (bcrypt), conexões SSL e armazenamento em nuvem com controle de acesso. Não garantimos segurança absoluta — nenhum sistema digital é 100% seguro.

**8. Contato**
Para exercer seus direitos ou tirar dúvidas: entre em contato pelo repositório do projeto no GitHub.

---

*Ao aceitar, você concorda com a coleta e uso dos seus dados conforme descrito acima.*
""".strip()


def render_termo_consentimento():
    """
    Exibe o termo de consentimento e bloqueia o acesso até aceitar.
    Retorna True se o usuário já consentiu, False caso contrário.
    """
    usuario_id = st.session_state.get("usuario_id")

    if not usuario_id:
        return False

    if usuario_consentiu(usuario_id):
        return True

    # bloqueia a tela com o termo
    st.markdown("## 📋 Termo de Consentimento")
    st.caption(f"Versão {VERSAO_ATUAL} — Leitura obrigatória antes de usar o MedTrack")

    with st.container(border=True):
        st.markdown(
            TERMO_TEXTO.format(versao=VERSAO_ATUAL),
            unsafe_allow_html=False
        )

    st.divider()

    aceito = st.checkbox(
        "Li e concordo com os Termos de Consentimento e Política de Privacidade do MedTrack Health AI"
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "✅ Aceitar e continuar",
            use_container_width=True,
            disabled=not aceito
        ):
            registrar_consentimento(usuario_id, aceito=True)
            st.session_state["consentimento_ok"] = True
            st.success("Consentimento registrado. Bem-vindo ao MedTrack!")
            st.rerun()

    with col2:
        if st.button(
            "❌ Recusar e sair",
            use_container_width=True,
            type="secondary"
        ):
            registrar_consentimento(usuario_id, aceito=False)
            st.session_state.clear()
            st.warning("Você recusou os termos. Sua sessão foi encerrada.")
            st.rerun()

    return False


def render_painel_privacidade():
    """
    Painel de privacidade: política, logs de acesso e direito ao esquecimento.
    """
    usuario_id = st.session_state["usuario_id"]

    tab_politica, tab_logs, tab_exclusao = st.tabs([
        "📄 Política de Privacidade",
        "🔍 Meus Logs de Acesso",
        "🗑️ Excluir Minha Conta"
    ])

    # ── Política de privacidade ──
    with tab_politica:
        st.markdown(
            TERMO_TEXTO.format(versao=VERSAO_ATUAL),
            unsafe_allow_html=False
        )

        st.divider()
        st.caption(
            f"Você aceitou estes termos na versão {VERSAO_ATUAL}. "
            "Se a política for atualizada, pediremos novo consentimento."
        )

    # ── Logs de acesso ──
    with tab_logs:
        st.markdown("#### Histórico de acessos e ações")
        st.caption(
            "Registramos suas ações para garantir transparência e segurança, "
            "conforme exigido pela LGPD."
        )

        logs = buscar_logs(usuario_id, limite=50)

        if not logs:
            st.info("Nenhum log registrado ainda.")
        else:
            ACOES_LABEL = {
                "login":               "🔐 Login realizado",
                "logout":              "🚪 Logout",
                "upload_exame":        "📤 Upload de exame",
                "visualizou_exame":    "👁️ Visualizou exame",
                "deletou_exame":       "🗑️ Excluiu exame",
                "upload_odonto":       "🦷 Upload odontológico",
                "solicitou_exclusao":  "⚠️ Solicitou exclusão de conta",
                "solicitou_exclusao_conta": "⚠️ Solicitou exclusão completa",
            }

            for log in logs:
                data = str(log["created_at"])[:16].replace("T", " ")
                acao = ACOES_LABEL.get(log["acao"], f"🔹 {log['acao']}")
                desc = f" — {log['descricao']}" if log.get("descricao") else ""
                st.markdown(
                    f"`{data}` &nbsp; {acao}{desc}",
                    unsafe_allow_html=True
                )

    # ── Direito ao esquecimento ──
    with tab_exclusao:
        st.markdown("#### Excluir minha conta e todos os dados")

        st.error(
            "⚠️ **Atenção: esta ação é irreversível.**\n\n"
            "Todos os seus dados serão permanentemente removidos:\n"
            "exames, laudos, histórico odontológico, perfil de saúde, "
            "alertas, embeddings e logs de acesso."
        )

        st.markdown(
            "Este é seu direito garantido pelo **Art. 18 da LGPD (Lei 13.709/2018)** — "
            "direito à eliminação dos dados pessoais tratados com consentimento."
        )

        st.divider()

        confirma = st.text_input(
            "Para confirmar, digite seu username abaixo:",
            placeholder="seu_username"
        )

        username_atual = st.session_state.get("usuario_nome", "")

        if st.button(
            "🗑️ Excluir permanentemente minha conta",
            type="primary",
            use_container_width=True,
            disabled=(confirma != username_atual)
        ):
            with st.spinner("Removendo todos os seus dados..."):
                excluir_todos_dados_usuario(usuario_id)
                st.session_state.clear()

            st.success(
                "Seus dados foram completamente removidos. "
                "Obrigado por usar o MedTrack."
            )
            st.rerun()

        if confirma and confirma != username_atual:
            st.caption("⚠️ Username incorreto.")
