from flask import Flask, send_from_directory, jsonify, request
import requests
import os

# Inicialização da aplicação Flask
# static_folder define onde estão os arquivos estáticos (HTML, CSS, JS)
app = Flask(__name__, static_folder='static')

# Configuração da URL do backend via variável de ambiente
# Em produção AWS: http://SEU_IP_PRIVADO_BACKEND:25000 (substitua pelo IP da instância backend)
# Em desenvolvimento: http://localhost:25000
BACKEND_URL = os.getenv('BACKEND_URL', 'http://localhost:25000')

@app.route('/')
def index():
    """
    Rota principal da aplicação
    Serve o arquivo index.html da pasta static
    
    Returns:
        HTML: Página principal da aplicação
    """
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/favicon.ico')
def favicon():
    """
    Endpoint para favicon
    Retorna resposta vazia para evitar erros 404 no navegador
    
    Returns:
        Empty response: Resposta vazia com código 204 (No Content)
    """
    return '', 204

@app.route('/api/birthdays')
def proxy_birthdays():
    """
    Proxy para o endpoint de todos os aniversários
    Faz requisição para o backend e retorna os dados para o frontend
    
    Returns:
        JSON: Lista de todos os aniversários com informações calculadas
        Error: Mensagem de erro se o backend estiver indisponível
    """
    try:
        # Requisição para o backend com timeout de 10 segundos
        response = requests.get(f'{BACKEND_URL}/api/birthdays', timeout=10)
        return jsonify(response.json())
    except requests.RequestException as e:
        # Retorna erro 500 se houver problema na comunicação
        return jsonify({"error": f"Backend indisponível: {str(e)}"}), 500

@app.route('/api/products')
def proxy_products():
    """
    Proxy para o endpoint de todos os produtos
    Faz requisição para o backend e retorna os dados para o frontend
    
    Returns:
        JSON: Lista de todos os produtos disponíveis
        Error: Mensagem de erro se o backend estiver indisponível
    """
    try:
        response = requests.get(f'{BACKEND_URL}/api/products', timeout=10)
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"Backend indisponível: {str(e)}"}), 500

@app.route('/api/products/lowstock')
def proxy_products_lowstock():
    """
    Proxy para o endpoint de produtos com estoque baixo
    
    Returns:
        JSON: Lista de produtos com estoque baixo
        Error: Mensagem de erro se o backend estiver indisponível
    """
    try:
        threshold = request.args.get('threshold', '10')
        response = requests.get(f'{BACKEND_URL}/api/products/lowstock?threshold={threshold}', timeout=10)
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"Backend indisponível: {str(e)}"}), 500

@app.route('/api/orders', methods=['POST'])
def proxy_orders():
    """
    Proxy para criar pedidos
    
    Returns:
        JSON: Resposta do backend sobre o pedido criado
        Error: Mensagem de erro se o backend estiver indisponível
    """
    try:
        data = request.get_json()
        response = requests.post(f'{BACKEND_URL}/api/orders', json=data, timeout=10)
        return jsonify(response.json()), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": f"Backend indisponível: {str(e)}"}), 500

@app.route('/api/birthdays/today')
def proxy_birthdays_today():
    """
    Proxy para o endpoint de aniversários de hoje
    
    Returns:
        JSON: Lista de aniversários que ocorrem hoje
        Error: Mensagem de erro se o backend estiver indisponível
    """
    try:
        response = requests.get(f'{BACKEND_URL}/api/birthdays/today', timeout=10)
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"Backend indisponível: {str(e)}"}), 500

@app.route('/api/birthdays/upcoming')
def proxy_birthdays_upcoming():
    """
    Proxy para o endpoint de próximos aniversários
    
    Returns:
        JSON: Lista de aniversários nos próximos 30 dias
        Error: Mensagem de erro se o backend estiver indisponível
    """
    try:
        response = requests.get(f'{BACKEND_URL}/api/birthdays/upcoming', timeout=10)
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({"error": f"Backend indisponível: {str(e)}"}), 500

@app.route('/health')
def health():
    """
    Endpoint de verificação de saúde (health check)
    Verifica se o frontend está funcionando e testa conectividade com o backend
    
    Returns:
        JSON: Status do frontend e backend
    """
    try:
        # Tenta conectar com o backend para verificar sua saúde
        backend_health = requests.get(f'{BACKEND_URL}/health', timeout=5)
        return jsonify({
            "frontend": "healthy",
            "backend": backend_health.json() if backend_health.status_code == 200 else "unhealthy"
        })
    except Exception:
        # Se não conseguir conectar com o backend, reporta como unhealthy
        return jsonify({
            "frontend": "healthy",
            "backend": "unhealthy"
        })

@app.route('/<path:filename>')
def static_files(filename):
    """
    Serve arquivos estáticos (CSS, JS, imagens, etc.)
    
    Args:
        filename (str): Nome do arquivo solicitado
        
    Returns:
        File: Arquivo estático da pasta static
    """
    return send_from_directory(app.static_folder, filename)

if __name__ == '__main__':
    """
    Ponto de entrada da aplicação
    Configura e inicia o servidor Flask
    
    Configurações:
    - host='0.0.0.0': Permite conexões de qualquer IP (necessário para Docker/AWS)
    - port=8080: Porta padrão configurada para o projeto
    - debug=True: Ativa modo de desenvolvimento com auto-reload
    """
    print("Iniciando Frontend - Lembretes de Aniversario")
    print("Rodando na porta 8080")
    print(f"Backend configurado para: {BACKEND_URL}")
    
    # Inicia o servidor Flask
    app.run(host='0.0.0.0', port=8080, debug=True)
