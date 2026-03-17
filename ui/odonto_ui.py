"""
UI para saúde bucal — odontograma interativo + upload de documentos odontológicos.
"""

import streamlit as st
import io
import os
from PIL import Image
from datetime import date

from services.odonto_service import extrair_dados_odonto
from services.document_reader import extrair_texto_documento
from services.storage_service import upload_arquivo
from repositories.odonto_repository import (
    salvar_registro_odonto,
    listar_registros_odonto,
    excluir_registro_odonto,
    buscar_odontograma,
    atualizar_dente,
    atualizar_odontograma_em_lote,
)

# ── Configuração do odontograma (numeração FDI) ──
DENTES_SUPERIOR = [18, 17, 16, 15, 14, 13, 12, 11, 21, 22, 23, 24, 25, 26, 27, 28]
DENTES_INFERIOR = [48, 47, 46, 45, 44, 43, 42, 41, 31, 32, 33, 34, 35, 36, 37, 38]

STATUS_CONFIG = {
    "saudavel":          {"cor": "#00C9A7", "emoji": "✅", "label": "Saudável"},
    "carie":             {"cor": "#E84545", "emoji": "🔴", "label": "Cárie"},
    "restaurado":        {"cor": "#2B7FD4", "emoji": "🔵", "label": "Restaurado"},
    "ausente":           {"cor": "#888888", "emoji": "⬜", "label": "Ausente"},
    "implante":          {"cor": "#6B3FA0", "emoji": "🟣", "label": "Implante"},
    "coroa":             {"cor": "#F5A623", "emoji": "🟡", "label": "Coroa"},
    "tratamento_canal":  {"cor": "#B85C00", "emoji": "🟠", "label": "Tratamento de canal"},
}

TIPOS_DOC = {
    "radiografia": "🔬 Radiografia",
    "laudo":       "📋 Laudo",
    "plano_tratamento": "📝 Plano de tratamento",
    "foto":        "📷 Foto intraoral",
}


def _cor_dente(numero, odontograma):
    status = odontograma.get(numero, {}).get("status", "saudavel")
    return STATUS_CONFIG.get(status, STATUS_CONFIG["saudavel"])["cor"]


def render_odontograma(usuario_id, odontograma):
    """Renderiza o odontograma SVG interativo."""

    # monta dados para o SVG
    def dente_info(numero):
        dado = odontograma.get(numero, {})
        status = dado.get("status", "saudavel")
        cfg    = STATUS_CONFIG.get(status, STATUS_CONFIG["saudavel"])
        obs    = dado.get("observacao") or cfg["label"]
        return cfg["cor"], cfg["emoji"], obs

    # gera SVG do odontograma
    svg_superior = ""
    svg_inferior = ""
    w = 36
    gap = 4
    total = len(DENTES_SUPERIOR)
    start_x = 20

    for i, num in enumerate(DENTES_SUPERIOR):
        x = start_x + i * (w + gap)
        cor, emoji, obs = dente_info(num)
        svg_superior += f"""
        <g class="dente" onclick="selecionarDente({num}, '{STATUS_CONFIG.get(odontograma.get(num, {}).get('status','saudavel'), STATUS_CONFIG['saudavel'])['label']}')">
          <rect x="{x}" y="10" width="{w}" height="{w}" rx="6"
                fill="{cor}" fill-opacity="0.18" stroke="{cor}" stroke-width="1.5"/>
          <text x="{x + w//2}" y="32" text-anchor="middle"
                font-size="11" fill="{cor}" font-weight="600">{num}</text>
        </g>"""

    for i, num in enumerate(DENTES_INFERIOR):
        x = start_x + i * (w + gap)
        cor, emoji, obs = dente_info(num)
        svg_inferior += f"""
        <g class="dente" onclick="selecionarDente({num}, '{STATUS_CONFIG.get(odontograma.get(num, {}).get('status','saudavel'), STATUS_CONFIG['saudavel'])['label']}')">
          <rect x="{x}" y="10" width="{w}" height="{w}" rx="6"
                fill="{cor}" fill-opacity="0.18" stroke="{cor}" stroke-width="1.5"/>
          <text x="{x + w//2}" y="32" text-anchor="middle"
                font-size="11" fill="{cor}" font-weight="600">{num}</text>
        </g>"""

    svg_width = start_x * 2 + total * (w + gap)

    st.components.v1.html(f"""
    <style>
      body {{ margin:0; font-family: 'DM Sans', sans-serif; background: transparent; }}
      .dente {{ cursor: pointer; transition: opacity 0.15s; }}
      .dente:hover {{ opacity: 0.75; }}
      .label {{ font-size:12px; fill:#6B8CB0; font-weight:500; }}
      #info-box {{
        margin-top: 12px;
        padding: 10px 14px;
        background: #F0F6FC;
        border-radius: 10px;
        border: 1px solid #C8DAEA;
        font-size: 13px;
        color: #1A2A6C;
        display: none;
      }}
    </style>

    <svg width="100%" viewBox="0 0 {svg_width} 100"
         xmlns="http://www.w3.org/2000/svg">

      <!-- Label superior -->
      <text x="{svg_width//2}" y="8" text-anchor="middle" class="label">
        Superior
      </text>
      {svg_superior}

      <!-- Label inferior -->
      <text x="{svg_width//2}" y="95" text-anchor="middle" class="label">
        Inferior
      </text>
    </svg>

    <!-- Linha inferior separada -->
    <svg width="100%" viewBox="0 0 {svg_width} 60"
         xmlns="http://www.w3.org/2000/svg">
      {svg_inferior}
    </svg>

    <div id="info-box">
      Dente <strong id="dente-num">—</strong>:
      <span id="dente-status">—</span>
    </div>

    <script>
    function selecionarDente(num, status) {{
      document.getElementById('info-box').style.display = 'block';
      document.getElementById('dente-num').textContent = num;
      document.getElementById('dente-status').textContent = status;
    }}
    </script>
    """, height=200)


def render_legenda():
    cols = st.columns(len(STATUS_CONFIG))
    for i, (key, cfg) in enumerate(STATUS_CONFIG.items()):
        with cols[i]:
            st.markdown(
                f"<div style='text-align:center;font-size:11px;"
                f"color:{cfg['cor']};font-weight:600'>"
                f"{cfg['emoji']}<br>{cfg['label']}</div>",
                unsafe_allow_html=True
            )


def render_odonto():
    usuario_id  = st.session_state["usuario_id"]
    odontograma = buscar_odontograma(usuario_id)

    tab_odo, tab_upload, tab_historico = st.tabs([
        "🦷 Odontograma", "📤 Novo Documento", "📋 Histórico"
    ])

    # ── Tab Odontograma ──
    with tab_odo:
        st.markdown("#### Mapa dental interativo")
        st.caption("Clique em um dente para ver seu status. Edite abaixo.")

        render_odontograma(usuario_id, odontograma)
        render_legenda()

        st.divider()
        st.markdown("#### Editar dente")

        col1, col2, col3 = st.columns([1, 2, 3])

        with col1:
            todos_dentes = DENTES_SUPERIOR + DENTES_INFERIOR
            dente_sel = st.selectbox(
                "Número do dente",
                sorted(todos_dentes)
            )

        with col2:
            status_atual = odontograma.get(dente_sel, {}).get("status", "saudavel")
            novo_status = st.selectbox(
                "Status",
                list(STATUS_CONFIG.keys()),
                index=list(STATUS_CONFIG.keys()).index(status_atual),
                format_func=lambda k: STATUS_CONFIG[k]["label"]
            )

        with col3:
            obs_atual = odontograma.get(dente_sel, {}).get("observacao", "")
            observacao = st.text_input("Observação", value=obs_atual or "")

        if st.button("💾 Salvar dente", type="primary"):
            atualizar_dente(usuario_id, dente_sel, novo_status, observacao or None)
            st.success(f"Dente {dente_sel} atualizado!")
            st.rerun()

    # ── Tab Upload ──
    with tab_upload:
        st.markdown("#### Enviar documento odontológico")

        arquivo = st.file_uploader(
            "Selecione o arquivo",
            type=["pdf", "png", "jpg", "jpeg"]
        )

        if not arquivo:
            st.info("Envie uma radiografia, laudo, plano de tratamento ou foto intraoral.")
            return

        conteudo = arquivo.read()
        arquivo.seek(0)

        ext = os.path.splitext(arquivo.name)[1].lower()
        if ext in [".png", ".jpg", ".jpeg"]:
            st.image(Image.open(io.BytesIO(conteudo)),
                     caption="Documento enviado", use_container_width=True)
        else:
            st.info("📄 PDF recebido.")
            st.download_button("Baixar PDF", data=conteudo,
                               file_name=arquivo.name, mime="application/pdf")

        with st.spinner("🤖 Analisando documento..."):
            texto   = extrair_texto_documento(arquivo)
            extraido = extrair_dados_odonto(texto)

        st.markdown("#### Confirme os dados")
        st.caption("A IA preencheu automaticamente. Corrija se necessário.")

        col1, col2 = st.columns(2)
        with col1:
            tipo_sel = st.selectbox(
                "Tipo de documento",
                list(TIPOS_DOC.keys()),
                index=list(TIPOS_DOC.keys()).index(extraido.get("tipo", "laudo"))
                      if extraido.get("tipo") in TIPOS_DOC else 0,
                format_func=lambda k: TIPOS_DOC[k]
            )
            dentista = st.text_input(
                "Dentista",
                value=extraido.get("dentista") or "",
                placeholder="Dr. Nome Sobrenome"
            )

        with col2:
            def _parse(d):
                if not d:
                    return None
                try:
                    p = d.split("-")
                    return date(int(p[0]), int(p[1]), int(p[2]))
                except Exception:
                    return None

            data_reg = st.date_input(
                "Data do documento",
                value=_parse(extraido.get("data_registro")),
                format="DD/MM/YYYY"
            )
            clinica = st.text_input(
                "Clínica / Consultório",
                value=extraido.get("clinica") or "",
                placeholder="Nome da clínica"
            )

        resumo = st.text_area(
            "Resumo / Observações",
            value=extraido.get("resumo") or "",
            height=100
        )

        # dentes afetados sugeridos pela IA
        dentes_ia = extraido.get("dentes_afetados", [])
        if dentes_ia:
            st.markdown(f"**A IA identificou {len(dentes_ia)} dente(s) afetado(s):**")
            for d in dentes_ia:
                cfg = STATUS_CONFIG.get(d.get("status", "saudavel"), STATUS_CONFIG["saudavel"])
                st.markdown(
                    f"- Dente **{d['numero']}**: {cfg['emoji']} {cfg['label']}"
                    + (f" — {d['observacao']}" if d.get("observacao") else "")
                )

            atualizar_odo = st.checkbox(
                "Atualizar odontograma automaticamente com esses dados", value=True
            )
        else:
            atualizar_odo = False

        if st.button("💾 Salvar documento", use_container_width=True):
            with st.spinner("Salvando..."):
                storage_path = upload_arquivo(usuario_id, arquivo.name, conteudo)

                salvar_registro_odonto(usuario_id, {
                    "tipo":           tipo_sel,
                    "subtipo":        extraido.get("subtipo"),
                    "nome_arquivo":   arquivo.name,
                    "texto_extraido": texto,
                    "resumo":         resumo,
                    "dentista":       dentista or None,
                    "clinica":        clinica or None,
                    "data_registro":  str(data_reg) if data_reg else None,
                }, storage_path=storage_path)

                if atualizar_odo and dentes_ia:
                    atualizar_odontograma_em_lote(usuario_id, dentes_ia)

            st.success("✅ Documento salvo com sucesso!")
            if atualizar_odo and dentes_ia:
                st.info(f"Odontograma atualizado com {len(dentes_ia)} dente(s).")
            st.rerun()

    # ── Tab Histórico ──
    with tab_historico:
        registros = listar_registros_odonto(usuario_id)

        if not registros:
            st.info("Nenhum documento odontológico ainda. Faça upload na aba ao lado.")
            return

        for reg in registros:
            tipo_label = TIPOS_DOC.get(reg["tipo"], reg["tipo"])
            data_str   = str(reg["data_registro"] or reg["created_at"])[:10]
            try:
                from datetime import datetime
                data_fmt = datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")
            except Exception:
                data_fmt = data_str

            titulo = f"{tipo_label}  —  {data_fmt}"
            if reg["dentista"]:
                titulo += f"  ·  {reg['dentista']}"

            with st.expander(titulo):
                if reg["clinica"]:
                    st.caption(f"🏥 {reg['clinica']}")
                st.write(reg["resumo"] or "Sem resumo.")

                if st.button("🗑️ Excluir", key=f"del_odonto_{reg['id']}",
                             type="secondary"):
                    excluir_registro_odonto(reg["id"])
                    st.success("Documento excluído.")
                    st.rerun()