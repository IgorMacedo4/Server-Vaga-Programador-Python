Web Content Analyzer with Gemini - Server

Este projeto é uma aplicação demonstrativa desenvolvida para evidenciar habilidades em automação web, integração avançada com IA (utilizando o modelo Gemini da Google Generative AI) e engenharia de dados.  
A API foi criada especialmente para a vaga de **Programador(a) Python** e permite extrair, analisar e salvar o conteúdo textual de páginas web.

---

## Visão Geral

A aplicação é construída em **Flask** e expõe uma série de endpoints que permitem:

- **Validar uma URL:** Verifica se a URL informada está no formato correto.
- **Analisar uma Página Web:** Realiza o scraping do conteúdo HTML, remove scripts, estilos e outros elementos indesejados, retornando um conteúdo textual limpo (snippet) e métricas de análise (contagem de links, títulos, parágrafos, etc.).
- **Interagir com um Chat Baseado em IA:** Permite que o usuário faça perguntas sobre o conteúdo extraído e receba respostas geradas pelo modelo **Gemini**.
- **Salvar o Conteúdo Extraído:** Oferece a opção de exportar o conteúdo textual limpo em formatos como **TXT, CSV, PDF** ou **JSON**.

---

## Funcionalidades

- **Validação de URL:**  
  Verifica se a URL possui o formato correto antes de processá-la.

- **Extração de Conteúdo:**  
  Utiliza as bibliotecas `requests` e `BeautifulSoup` para realizar o scraping e limpar o HTML da página.

- **Análise Estrutural:**  
  Conta elementos importantes da página, como links, títulos, parágrafos, tabelas, imagens e listas.

- **Integração com IA:**  
  Utiliza o modelo **Gemini** da Google Generative AI para gerar respostas e sugestões com base no conteúdo extraído.

- **Geração de Arquivos:**  
  Permite salvar o conteúdo extraído em formatos **TXT, CSV, PDF** ou **JSON** usando a biblioteca `FPDF` (para PDF) e outras ferramentas de formatação.

- **Configuração de CORS:**  
  Configurado para permitir requisições provenientes do front-end (exemplo: `https://front-vaga-programador-python.vercel.app`).

---

## Tecnologias Utilizadas

- **Flask** – Framework web para criação da API.
- **Flask-CORS** – Para gerenciamento de CORS.
- **Requests** – Para fazer requisições HTTP.
- **BeautifulSoup** – Para parsing e extração de dados do HTML.
- **FPDF** – Para gerar arquivos PDF.
- **Google Generative AI (Gemini)** – Para geração de conteúdo via IA.
- **Python-dotenv** – Para carregar variáveis de ambiente a partir de um arquivo `.env`.

---

## Instalação e Execução

### 1. Clone o Repositório

```bash
git clone https://github.com/IgorMacedo4/Server-Vaga-Programador-Python.git
cd Server-Vaga-Programador-Python
```

### 2. Crie e Ative um Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate  # Para Linux/Mac
venv\Scripts\activate     # Para Windows
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:

```
GOOGLE_API_KEY=your_google_api_key_here
FLASK_ENV=development
```

### 5. Inicie o Servidor

```bash
python app.py
```

O servidor ficará disponível em:
[http://localhost:5000](http://localhost:5000)

---

## Endpoints da API

### **GET /validate?url=<url>**

**Descrição:**
Valida se a URL informada está no formato correto.

**Exemplo:**

```bash
GET http://localhost:5000/validate?url=https://www.exemplo.com
```

**Resposta Exemplo:**

```json
{ "valid": true }
```

### **POST /analyze**

**Corpo Esperado (JSON):**

```json
{ "url": "https://www.exemplo.com" }
```

**Resposta Exemplo:**

```json
{
  "snippet": "Resumo do conteúdo...",
  "full_content": "Conteúdo textual limpo extraído da página...",
  "analysis": { "links": 10, "titulos": 3, "paragrafos": 20 },
  "suggestions": ["- 10 links encontrados", "- 3 títulos e cabeçalhos"],
  "gemini_suggestions": "Sugestão 1...\nSugestão 2...",
  "execution_time": 0.45
}
```

### **POST /ask**

**Corpo Esperado (JSON):**

```json
{
  "url": "https://www.exemplo.com",
  "question": "Sua pergunta",
  "data_type": "tudo"
}
```

**Resposta Exemplo:**

```json
{
  "question": "Sua pergunta",
  "response": "Resposta gerada pelo modelo Gemini..."
}
```

### **POST /save**

**Corpo Esperado (JSON):**

```json
{
  "content": "Conteúdo extraído",
  "format_type": "pdf",
  "filename_base": "output"
}
```

---

## Deploy

**Repositório Git:**
[https://github.com/IgorMacedo4/Server-Vaga-Programador-Python.git](https://github.com/IgorMacedo4/Server-Vaga-Programador-Python.git)

**Deploy na Render:**
[https://server-vaga-programador-python.onrender.com](https://server-vaga-programador-python.onrender.com)

---

## Considerações Finais

Esta aplicação demonstra a integração de técnicas de web scraping com a geração de respostas via IA e a exportação dos dados extraídos em múltiplos formatos.

Desenvolvido por Igor Macedo para a vaga de Programador(a) Python.

