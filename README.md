
# 🤖 Chatbot Inteligente com IA Generativa e RAG 🧠

Bora conhecer esse projeto massa? 🚀 Aqui criei um chatbot que usa IA generativa com RAG (Retorno por Recuperação) pra responder às perguntas com base num banco de dados vetorial! E é todo trabalhado no Flask, LangChain e OpenAI! 😎

---

## 🌟 Recursos Principais

- **🧠 IA Generativa:** Respostas inteligentes e no ponto, direto do modelo `gpt-3.5-turbo`.
- **📚 Recuperação de Respostas (RAG):** Busca as informações onde estão e devolve pra ti.
- **💻 Interface Web:** Uma cara bonita e fácil pra bater papo com o robô.
- **📂 Gerenciamento de Documentos:** Lê PDFs e guarda tudo no banco de dados vetorial. Fino, né?

---

## 🗂️ Estrutura do Projeto

```plaintext
├── main.py                     # O coração do chatbot (backend)
├── vector_database_manager.py  # Processa e organiza os dados vetoriais
├── static/
│   ├── script.js               # Faz a magia do chat acontecer no navegador
│   ├── styles.css              # Estilo pra ficar chique
│   ├── user-avatar.png         # Um avatarzinho pra ficar bonito
│   └── fametro-avatar.png      # Outro avatarzinho pra ficar bonito
├── templates/
│   └── index.html              # A página principal do chat
├── pdfs/                       # Aqui ficam os PDFs pra processar
├── vectorstore/                # Base de dados vetorial gerada
├── requirements.txt            # Todos os programas a serem instalados
└── README.md                   # Tu tá lendo ele agora!
```

---

## 🚀 Como Rodar o Projeto

### 📋 O que tu precisa?

- **Python 3.10 ou superior** (versão moderna, viu?)
- **API Key da OpenAI:** Vai lá no [site da OpenAI](https://openai.com) e pega a tua.
- Instalar as dependências: Dá-lhe esse comando:
  ```bash
  pip install -r requirements.txt
  ```

---

### 🎯 Passo a Passo Pra Rodar

1. **Configurar o Ambiente:** Cria um arquivo `.env` com tua chave API:
   ```plaintext
   OPENAI_API_KEY=your_api_key_here
   ```

2. **Processar os PDFs:** Joga teus arquivos na pasta `pdfs/` e roda:
   ```bash
   python vector_database_manager.py
   ```

3. **Subir o Servidor:** Agora, é só botar o Flask pra funcionar:
   ```bash
   python main.py
   ```

4. **Abrir no Navegador:** Vai lá no endereço [http://localhost:5000](http://localhost:5000) e aproveita.

---

## 🎨 Funcionalidades Show de Bola

- **🕵️ Busca Inteligente:** Ele vasculha o banco vetorial e traz só o que interessa.
- **💬 Respostas Contextuais:** Tudo ajustado ao contexto, pra não ficar perdido.
- **🖥️ Chat Interativo:** Interface moderna e responsiva, do jeito que o povo gosta.
- **📖 Processamento de PDFs:** Ele lê, entende e organiza os documentos rapidinho.

---

Pronto, tá tudo aí, facinho de usar. Agora bora codar e aproveitar esse chatbot arretado! 😄
