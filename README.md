# 🩺 MedTrack Health AI

> Seu copiloto inteligente de saúde — centralize, interprete e consulte seus exames médicos com IA.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-3ECF8E?style=flat-square&logo=supabase&logoColor=white)
![Groq](https://img.shields.io/badge/LLM-Groq-F55036?style=flat-square)
![License](https://img.shields.io/badge/status-MVP-blue?style=flat-square)

---

## 📌 Sobre o projeto

O **MedTrack Health AI** resolve um problema muito comum: pessoas possuem exames espalhados em PDFs, fotos e sistemas diferentes, sem uma forma simples de acompanhar sua evolução clínica.

A aplicação atua como um **Health Intelligence Assistant** — transforma documentos médicos desorganizados em dados estruturados e consultáveis, permitindo que o usuário acompanhe sua saúde ao longo do tempo e faça perguntas sobre seus próprios exames em linguagem natural.

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|---|---|
| 🔐 **Autenticação** | Cadastro e login com hash seguro de senha (bcrypt) |
| 📤 **Upload de exames** | Suporte a PDF e imagens com armazenamento em cloud |
| 🔍 **Extração de texto** | OCR automático via PyMuPDF e Tesseract |
| 🤖 **Resumo por IA** | Interpretação automática do exame em linguagem simples |
| 📊 **Valores estruturados** | Extração de parâmetros laboratoriais (hemoglobina, leucócitos, etc.) |
| 📈 **Evolução temporal** | Gráficos de tendência por parâmetro ao longo do tempo |
| ⚠️ **Alertas clínicos** | Notificações automáticas para valores fora da referência |
| 🗂️ **Timeline de saúde** | Histórico cronológico de exames por categoria |
| 💬 **Chat inteligente** | Perguntas em linguagem natural respondidas com base nos seus exames |

---

## 🏗️ Arquitetura

```
medtrack-health-ai/
│
├── app.py                        # Entrypoint da aplicação
│
├── auth/
│   ├── auth_service.py           # Lógica de login e registro
│   └── login_ui.py               # Interface de autenticação
│
├── database/
│   └── db.py                     # Conexão PostgreSQL (Supabase)
│
├── models/
│   └── exame.py                  # Entidade Exame
│
├── repositories/
│   ├── usuario_repository.py     # CRUD de usuários
│   ├── exame_repository.py       # CRUD de exames
│   ├── valores_repository.py     # Valores laboratoriais estruturados
│   └── alertas_repository.py     # Alertas clínicos
│
├── services/
│   ├── ai_service.py             # Integração com Groq LLM
│   ├── chat_service.py           # Lógica do chat de saúde
│   ├── document_reader.py        # Extração de texto (OCR)
│   ├── exame_classifier.py       # Classificação automática de exames
│   ├── exame_service.py          # Pipeline principal de processamento
│   ├── extracao_service.py       # Extração estruturada de valores
│   ├── embedding_service.py      # Geração de embeddings semânticos
│   └── storage_service.py        # Upload para Supabase Storage
│
├── rag/
│   └── vector_store.py           # Busca semântica via pgvector
│
├── ui/
│   ├── upload_ui.py              # Tela de upload
│   ├── timeline_ui.py            # Timeline de exames
│   ├── chat_ui.py                # Interface do chat
│   ├── valores_ui.py             # Tabela e gráfico de valores
│   └── alertas_ui.py             # Painel de alertas clínicos
│
└── utils/
    ├── security.py               # Utilitários de segurança
    └── pdf_parser.py             # Parser de PDFs
```

---

## 🔄 Pipeline de processamento

```
Upload do arquivo
       ↓
Extração de texto (OCR)
       ↓
Resumo interpretado pela IA
       ↓
Classificação da categoria
       ↓
Upload para Supabase Storage
       ↓
Salvamento dos metadados no PostgreSQL
       ↓
Extração de valores estruturados
       ↓
Geração de alertas clínicos
       ↓
Indexação do embedding no pgvector
       ↓
Exame disponível na timeline e no chat
```

---

## 🛠️ Stack tecnológica

### Backend e aplicação
- **Python 3.11**
- **Streamlit** — interface web

### Banco de dados
- **PostgreSQL** via **Supabase** — dados relacionais
- **pgvector** — busca semântica vetorial
- **Supabase Storage** — armazenamento de arquivos

### Inteligência Artificial
- **Groq API** — LLM para resumos, extração e chat
- **Sentence Transformers** (`all-MiniLM-L6-v2`) — embeddings semânticos

### Processamento de documentos
- **PyMuPDF** — leitura de PDFs
- **pytesseract + Tesseract OCR** — leitura de imagens

### Segurança
- **bcrypt** — hash de senhas
- **Streamlit Secrets** — gestão de credenciais

---

## 🚀 Como rodar localmente

### Pré-requisitos

- Python 3.11+
- Tesseract OCR instalado ([instruções](https://github.com/tesseract-ocr/tesseract))
- Conta no [Supabase](https://supabase.com)
- Chave de API no [Groq](https://console.groq.com)

### Instalação

```bash
# Clone o repositório
git clone https://github.com/Guilhermepe1/medtrack-health-ai.git
cd medtrack-health-ai

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instale as dependências
pip install -r requirements.txt
```

### Configuração

Crie o arquivo `.streamlit/secrets.toml`:

```toml
DB_HOST         = "seu-host.supabase.com"
DB_USER         = "postgres.seu-projeto"
DB_PASSWORD     = "sua-senha"
SUPABASE_URL    = "https://seu-projeto.supabase.co"
SUPABASE_SERVICE_KEY = "sua-service-key"
GROQ_API_KEY    = "sua-chave-groq"
```

### Banco de dados

Execute os scripts SQL no Supabase SQL Editor:

```sql
-- Extensão vetorial
CREATE EXTENSION IF NOT EXISTS vector;

-- Tabela de usuários
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    senha TEXT NOT NULL
);

-- Tabela de exames
CREATE TABLE exames (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    arquivo VARCHAR(255),
    texto TEXT,
    resumo TEXT,
    categoria VARCHAR(100),
    storage_path TEXT,
    data_upload TIMESTAMP DEFAULT NOW()
);

-- Embeddings vetoriais
CREATE TABLE exame_embeddings (
    id SERIAL PRIMARY KEY,
    exame_id INTEGER REFERENCES exames(id) ON DELETE CASCADE,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    embedding vector(384)
);

-- Valores laboratoriais estruturados
CREATE TABLE exame_valores (
    id SERIAL PRIMARY KEY,
    exame_id INTEGER REFERENCES exames(id) ON DELETE CASCADE,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    parametro VARCHAR(100),
    valor NUMERIC,
    unidade VARCHAR(50),
    referencia_min NUMERIC,
    referencia_max NUMERIC,
    status VARCHAR(20),
    data_coleta DATE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Alertas clínicos
CREATE TABLE alertas_clinicos (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id) ON DELETE CASCADE,
    exame_id INTEGER REFERENCES exames(id) ON DELETE CASCADE,
    parametro VARCHAR(100),
    valor NUMERIC,
    unidade VARCHAR(50),
    referencia_min NUMERIC,
    referencia_max NUMERIC,
    status VARCHAR(20),
    lido BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Executar

```bash
streamlit run app.py
```

Acesse em `http://localhost:8501`

---

## ☁️ Deploy

A aplicação está publicada no **Streamlit Community Cloud**.

Pipeline de deploy automático:

```
Push no GitHub → Deploy automático no Streamlit Cloud
```

Para configurar o seu próprio deploy:

1. Faça fork do repositório
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte o repositório
4. Configure os Secrets no painel do Streamlit Cloud
5. Deploy!

---

## 🗺️ Roadmap

- [x] Autenticação com bcrypt
- [x] Upload de PDFs e imagens
- [x] Resumo automático por IA
- [x] Timeline de exames
- [x] Chat inteligente com RAG (pgvector)
- [x] Extração estruturada de valores laboratoriais
- [x] Alertas clínicos automáticos
- [x] Supabase Storage para arquivos
- [ ] Histórico multi-turno no chat
- [ ] Dashboard com métricas de saúde
- [ ] OAuth / Login com Google
- [ ] Compartilhamento de exame com médico
- [ ] Relatório em PDF exportável
- [ ] API pública para integração com clínicas

---

## ⚠️ Aviso importante

O MedTrack Health AI é uma ferramenta de **apoio informacional** e **não substitui consulta médica**. As interpretações geradas pela IA têm caráter educativo. Sempre consulte um profissional de saúde para diagnósticos e decisões clínicas.

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<p align="center">Desenvolvido com ❤️ e IA</p>
