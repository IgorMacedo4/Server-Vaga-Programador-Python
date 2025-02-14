import os
import time
import json
import csv
from io import BytesIO, StringIO

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from fpdf import FPDF
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import google.generativeai as genai
from dotenv import load_dotenv

# Carregar variáveis de ambiente do .env
load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise Exception("GOOGLE_API_KEY não encontrada no arquivo .env.")

# Configurar a API do Gemini
genai.configure(api_key=GOOGLE_API_KEY)

app = Flask(__name__)
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:5173"],  # Adicione seu domínio React
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "supports_credentials": True
    }
})

class WebContentAnalyzer:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def validate_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def extract_initial_content(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # Remove elementos indesejados
            for element in soup(['script', 'style', 'iframe', 'meta', 'noscript']):
                element.decompose()
            return soup
        except Exception as e:
            print(f"Erro ao extrair conteúdo: {str(e)}")
            return None

    def extract_specific_content(self, soup, data_type):
        try:
            dt = data_type.lower()
            if dt == 'links':
                return [link.get('href') for link in soup.find_all('a', href=True)]
            elif dt in ['títulos', 'titulos']:
                return [h.get_text().strip() for h in soup.find_all(['h1', 'h2', 'h3'])]
            elif dt in ['parágrafos', 'paragrafos']:
                return [p.get_text().strip() for p in soup.find_all('p')]
            elif dt == 'tudo':
                return soup.get_text().strip()
            else:
                return soup.get_text().strip()
        except Exception as e:
            print(f"Erro ao extrair conteúdo específico: {str(e)}")
            return None

    def analyze_content_structure(self, soup):
        try:
            analysis = {
                'links': len(soup.find_all('a', href=True)),
                'titulos': len(soup.find_all(['h1', 'h2', 'h3'])),
                'paragrafos': len(soup.find_all('p')),
                'tabelas': len(soup.find_all('table')),
                'imagens': len(soup.find_all('img')),
                'listas': len(soup.find_all(['ul', 'ol']))
            }
            return analysis
        except Exception as e:
            print(f"Erro ao analisar estrutura: {str(e)}")
            return None

    def suggest_extractions(self, analysis):
        suggestions = []
        if analysis.get('links', 0) > 0:
            suggestions.append(f"- {analysis['links']} links encontrados")
        if analysis.get('titulos', 0) > 0:
            suggestions.append(f"- {analysis['titulos']} títulos e cabeçalhos")
        if analysis.get('paragrafos', 0) > 0:
            suggestions.append(f"- {analysis['paragrafos']} parágrafos de texto")
        if analysis.get('tabelas', 0) > 0:
            suggestions.append(f"- {analysis['tabelas']} tabelas")
        if analysis.get('imagens', 0) > 0:
            suggestions.append(f"- {analysis['imagens']} imagens")
        if analysis.get('listas', 0) > 0:
            suggestions.append(f"- {analysis['listas']} listas")
        return suggestions

    def ask_gemini(self, content, question):
        try:
            prompt = f"""
Com base no seguinte conteúdo:
{content}

Por favor, responda: {question}
"""
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Erro ao consultar o Gemini: {str(e)}"

analyzer = WebContentAnalyzer()

@app.route('/validate', methods=['GET'])
def validate():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Parâmetro 'url' é obrigatório."}), 400
    valid = analyzer.validate_url(url)
    return jsonify({"valid": valid})

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    url = data.get('url')
    if not url or not analyzer.validate_url(url):
        return jsonify({"error": "URL inválida ou ausente."}), 400

    start_time = time.time()
    soup = analyzer.extract_initial_content(url)
    if soup is None:
        return jsonify({"error": "Não foi possível extrair o conteúdo da URL."}), 500

    analysis = analyzer.analyze_content_structure(soup)
    suggestions_list = analyzer.suggest_extractions(analysis)
    execution_time = time.time() - start_time

    # Captura apenas o conteúdo de texto limpo
    text_content = soup.get_text(separator="\n", strip=True)
    snippet = text_content[:1000] + ("..." if len(text_content) > 1000 else "")

    # Geração de sugestões pelo Gemini usando somente o texto
    prompt = f"""
Analise o seguinte conteúdo de página web (apenas texto, sem CSS ou JS):
{text_content[:1500]}

Além disso, foram identificados os seguintes elementos:
{chr(10).join(suggestions_list)}

Você pode salvar este conteúdo se desejar. Sugira 3-4 perguntas interessantes que o usuário poderia fazer sobre esse conteúdo.
Seja conciso e direto.
"""
    gemini_response = analyzer.model.generate_content(prompt)
    gemini_suggestions = gemini_response.text if gemini_response else "Nenhuma sugestão gerada."

    return jsonify({
        "snippet": snippet,
        "full_content": text_content,  # Retorna o texto limpo
        "analysis": analysis,
        "suggestions": suggestions_list,
        "gemini_suggestions": gemini_suggestions,
        "execution_time": execution_time
    })



@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    url = data.get('url')
    question = data.get('question')
    data_type = data.get('data_type', 'tudo')
    if not url or not question or not analyzer.validate_url(url):
        return jsonify({"error": "URL ou pergunta inválida/ausente."}), 400

    soup = analyzer.extract_initial_content(url)
    if soup is None:
        return jsonify({"error": "Não foi possível extrair o conteúdo da URL."}), 500

    content = analyzer.extract_specific_content(soup, data_type)
    gemini_response = analyzer.ask_gemini(content, question)
    return jsonify({
        "question": question,
        "response": gemini_response
    })

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    content = data.get('content')
    format_type = data.get('format_type')
    filename_base = data.get('filename_base', 'output')
    if not content or not format_type:
        return jsonify({"error": "Os parâmetros 'content' e 'format_type' são obrigatórios."}), 400

    format_type = format_type.lower()

    if format_type == 'txt':
        file_stream = StringIO()
        file_stream.write(str(content))
        file_stream.seek(0)
        output = BytesIO(file_stream.getvalue().encode('utf-8'))
        mime = 'text/plain'
        extension = 'txt'

    elif format_type == 'csv':
        csv_stream = StringIO()
        csv_writer = csv.writer(csv_stream)
        csv_writer.writerow([content])
        csv_data = csv_stream.getvalue()
        output = BytesIO(csv_data.encode('utf-8'))
        mime = 'text/csv'
        extension = 'csv'

# Modifique a parte do PDF na função save:
    elif format_type == 'pdf':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Função para limpar o texto de caracteres problemáticos
        def clean_text(text):
            # Substitui caracteres problemáticos por equivalentes ASCII
            replacements = {
                '\u2013': '-',  # en dash
                '\u2014': '-',  # em dash
                '\u2018': "'",  # aspas simples esquerda
                '\u2019': "'",  # aspas simples direita
                '\u201c': '"',  # aspas duplas esquerda
                '\u201d': '"',  # aspas duplas direita
                '\u2026': '...',  # reticências
                '\u00a0': ' ',  # espaço não-quebrável
                '\u200b': '',   # zero-width space
            }
            
            for old, new in replacements.items():
                text = text.replace(old, new)
            
            # Remove outros caracteres que não podem ser codificados em latin1
            return ''.join(char for char in text if ord(char) < 256)
        
        # Limpa o texto antes de adicionar ao PDF
        cleaned_content = clean_text(str(content))
        
        # Divide o texto em linhas menores para evitar overflow
        lines = cleaned_content.split('\n')
        for line in lines:
            # Divide linhas muito longas
            while len(line) > 0:
                chunk = line[:80]  # Ajuste este número conforme necessário
                pdf.multi_cell(0, 10, txt=chunk)
                line = line[80:]
                
        output = BytesIO(pdf.output(dest='S').encode('latin1', errors='replace'))
        mime = 'application/pdf'
        extension = 'pdf'

    elif format_type == 'json':
        json_content = json.dumps(content, ensure_ascii=False, indent=2)
        output = BytesIO(json_content.encode('utf-8'))
        mime = 'application/json'
        extension = 'json'
    else:
        return jsonify({"error": "Formato não suportado."}), 400

    filename = f"{filename_base}.{extension}"
    output.seek(0)
    return send_file(output, mimetype=mime, as_attachment=True, download_name=filename)



if __name__ == '__main__':
    app.run(debug=True)
