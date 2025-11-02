# Backend Dockerfile para Candy Shop API
# Configura container para a API Flask que gerencia produtos de doces

# Usa imagem base Python 3.11 slim
# Escolha baseada em compatibilidade e tamanho otimizado
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia arquivo de dependências primeiro para otimizar cache do Docker
# Se requirements.txt não mudar, esta camada será reutilizada
COPY requirements.txt .

# Instala dependências Python
# --no-cache-dir: remove cache do pip para reduzir tamanho final da imagem
RUN pip install --no-cache-dir -r requirements.txt

# Copia código fonte da aplicação API
COPY app.py .

# Expõe porta 25000 para comunicação interna
# Porta configurada especificamente para este projeto
# Acessível apenas pelo frontend na arquitetura AWS
EXPOSE 25000

# Comando padrão ao iniciar o container
# Executa a API Flask quando o container for iniciado
CMD ["python", "app.py"]
