# Frontend Dockerfile para Birthday Reminder
# Configura container para servir a aplicação web Flask

# Usa imagem base Python 3.11 slim para menor tamanho
FROM python:3.11-slim

# Define diretório de trabalho dentro do container
WORKDIR /app

# Copia arquivo de dependências primeiro (para aproveitar cache do Docker)
COPY requirements.txt .

# Instala dependências Python
# --no-cache-dir: não mantém cache local para reduzir tamanho da imagem
RUN pip install --no-cache-dir -r requirements.txt

# Copia código fonte da aplicação
COPY app.py .

# Copia arquivos estáticos (HTML, CSS, JS)
COPY static/ ./static/

# Expõe porta 8080 para acesso externo
# Esta é a porta configurada para o frontend
EXPOSE 8080

# Comando para iniciar a aplicação
# Executa o servidor Flask quando o container for iniciado
CMD ["python", "app.py"]
