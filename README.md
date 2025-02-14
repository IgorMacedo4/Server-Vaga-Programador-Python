# Web Content Analyzer with Gemini

Este projeto é uma aplicação demonstrativa desenvolvida para evidenciar habilidades em automação web, integração avançada com IA (usando o modelo Gemini da Google Generative AI) e engenharia de dados. Ele foi criado especialmente para a vaga de Programador(a) Python e pode ser usado para extrair, analisar e salvar o conteúdo de páginas web.

---

## 📌 Visão Geral

A aplicação é construída em **Flask** e expõe uma série de endpoints que permitem:

✅ **Validar uma URL:** Verificar se a URL informada está no formato correto.

✅ **Analisar uma Página Web:** Extrair e limpar o conteúdo textual da página (removendo scripts, estilos, etc.) e gerar um resumo (**snippet**) junto com métricas de análise (como contagem de links, títulos, parágrafos, etc.).

✅ **Interagir com um Chat Baseado em IA:** Permitir que o usuário faça perguntas sobre o conteúdo extraído e receba respostas geradas pelo modelo **Gemini**.

✅ **Salvar o Conteúdo Extraído:** Oferecer a opção de baixar o conteúdo textual limpo em vários formatos (**TXT, CSV, PDF, JSON**).

---

## 🚀 Funcionalidades

- **🔍 Validação de URL** - Verifica se a URL possui o formato correto antes de processá-la.
- **📜 Extração de Conteúdo** - Utiliza as bibliotecas `requests` e `BeautifulSoup` para fazer o scraping e limpar o HTML da página.
- **📊 Análise Estrutural** - Conta elementos importantes da página, como links, títulos, parágrafos, tabelas, imagens e listas.
- **🤖 Integração com IA** - Usa o modelo **Gemini** para gerar respostas e sugestões baseadas no conteúdo extraído.
- **💾 Geração de Arquivos** - Permite salvar o conteúdo extraído em formatos **TXT, CSV, PDF** ou **JSON** utilizando a biblioteca `FPDF`.
- **🌍 CORS Configurado** - Configurado para permitir requisições provenientes do front-end (exemplo: `http://localhost:5173`).

---

## 🛠️ Tecnologias Utilizadas

- **🖥️ Flask** - Framework web para criação da API.
- **🔗 Flask-CORS** - Para gerenciamento de CORS.
- **🌐 Requests** - Para fazer requisições HTTP.
- **📄 BeautifulSoup** - Para parsing e extração de dados do HTML.
- **📑 FPDF** - Para gerar arquivos PDF.
- **🧠 Google Generative AI (Gemini)** - Para geração de conteúdo via IA.
- **⚙️ Python-dotenv** - Para carregar variáveis de ambiente a partir de um arquivo `.env`.

---

## 📥 Instalação e Execução

### 1️⃣ Clone o repositório:
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

### 2️⃣ Crie e ative um ambiente virtual:
```bash
python3 -m venv venv
source venv/bin/activate  # Para Linux/Mac
venv\Scripts\activate     # Para Windows
```

### 3️⃣ Instale as dependências:
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
```env
GOOGLE_API_KEY=your_google_api_key_here
FLASK_ENV=development
```

### 5️⃣ Inicie o servidor:
```bash
python app.py
```
O servidor estará disponível em **[http://localhost:5000](http://localhost:5000)**.

---

## 📡 Endpoints da API

### 🔹 **GET /validate?url=<url>**
📌 Valida o formato da URL informada.

### 🔹 **POST /analyze**
📌 Corpo esperado (**JSON**):
```json
{
  "url": "https://www.exemplo.com"
}
```
📌 Retorna:
- Um snippet do conteúdo textual limpo da página.
- Métricas de análise (**links, títulos, parágrafos, etc.**).
- Sugestões geradas pelo modelo **Gemini**.

### 🔹 **POST /ask**
📌 Corpo esperado (**JSON**):
```json
{
  "url": "https://www.exemplo.com",
  "question": "Sua pergunta",
  "data_type": "tudo"
}
```
📌 Retorna a resposta do modelo **Gemini** para a pergunta feita com base no conteúdo extraído.

### 🔹 **POST /save**
📌 Corpo esperado (**JSON**):
```json
{
  "content": "Conteúdo extraído",
  "format_type": "pdf",
  "filename_base": "output"
}
```
📌 Inicia o download do conteúdo no formato especificado.

---

## 📢 Considerações Finais

Esta aplicação demonstra a integração de técnicas de **web scraping** com a capacidade de gerar respostas via **IA**, além de possibilitar a exportação dos dados extraídos em múltiplos formatos.

Foi desenvolvida para atender às exigências de uma vaga de **Programador(a) Python** com experiência em **automação web** e aplicações avançadas com IA.

📌 **Desenvolvido por Igor Macedo** para a vaga de **Programador(a) Python**. Este demonstrativo foi enviado exclusivamente para **thomas.maia@abladvogados.com**.

---

## 🎯 Como Usar

- **Clone o repositório** e siga as instruções de instalação para executar o servidor localmente.
- **Interaja com os endpoints** usando o front-end (que será desenvolvido separadamente).

