from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import json

# Inicialização da aplicação Flask
app = Flask(__name__)

# Habilita CORS para permitir requisições do frontend
# Necessário para comunicação entre containers Docker
CORS(app)

# Base de dados simples de produtos em memória
# Em produção, seria substituído por banco de dados real
products_db = [
    {"id": 1, "name": "Brigadeiro Gourmet", "category": "doce", "flavor": "chocolate", "price": 3.50, "stock": 25},
    {"id": 2, "name": "Beijinho Premium", "category": "doce", "flavor": "coco", "price": 3.50, "stock": 20},
    {"id": 3, "name": "Torta de Chocolate", "category": "torta", "flavor": "chocolate", "price": 45.00, "stock": 5},
    {"id": 4, "name": "Torta de Morango", "category": "torta", "flavor": "morango", "price": 48.00, "stock": 3},
    {"id": 5, "name": "Quindim", "category": "doce", "flavor": "coco", "price": 4.00, "stock": 15},
    {"id": 6, "name": "Pudim de Leite", "category": "doce", "flavor": "caramelo", "price": 35.00, "stock": 8},
    {"id": 7, "name": "Torta de Limão", "category": "torta", "flavor": "limão", "price": 42.00, "stock": 2},
    {"id": 8, "name": "Trufa de Chocolate", "category": "doce", "flavor": "chocolate", "price": 2.50, "stock": 50},
]

# Contador para IDs de pedidos
next_order_id = 1
orders_db = []

@app.route('/health')
def health_check():
    """Endpoint de verificação de saúde"""
    return jsonify({
        "status": "healthy",
        "service": "Candy Shop API",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/products')
def get_all_products():
    """Retorna todos os produtos disponíveis"""
    return jsonify({
        "products": products_db,
        "total": len(products_db)
    })

@app.route('/api/products/lowstock')
def get_lowstock_products():
    """Retorna produtos com estoque baixo"""
    threshold = int(request.args.get('threshold', 10))
    
    lowstock_products = [p for p in products_db if p['stock'] <= threshold]
    
    return jsonify({
        "products": lowstock_products,
        "count": len(lowstock_products),
        "threshold": threshold
    })

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Cria um novo pedido"""
    global next_order_id
    
    try:
        data = request.get_json()
        
        if not data or 'items' not in data:
            return jsonify({"error": "Items são obrigatórios"}), 400
            
        items = data['items']
        customer = data.get('customer', {})
        
        # Validar items e calcular total
        order_items = []
        total = 0
        
        for item in items:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 1)
            
            # Encontrar produto
            product = next((p for p in products_db if p['id'] == product_id), None)
            if not product:
                return jsonify({"error": f"Produto {product_id} não encontrado"}), 404
                
            # Verificar estoque
            if product['stock'] < quantity:
                return jsonify({"error": f"Estoque insuficiente para {product['name']}"}), 400
            
            # Calcular subtotal
            subtotal = product['price'] * quantity
            total += subtotal
            
            order_items.append({
                "product_id": product_id,
                "product_name": product['name'],
                "quantity": quantity,
                "unit_price": product['price'],
                "subtotal": subtotal
            })
            
            # Reduzir estoque
            product['stock'] -= quantity
        
        # Criar pedido
        order = {
            "id": next_order_id,
            "customer": customer,
            "items": order_items,
            "total": round(total, 2),
            "created_at": datetime.now().isoformat()
        }
        
        orders_db.append(order)
        next_order_id += 1
        
        return jsonify({
            "success": True,
            "order": order
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Iniciando API da Loja de Doces")
    print("Rodando na porta 25000")
    app.run(host='0.0.0.0', port=25000, debug=True)