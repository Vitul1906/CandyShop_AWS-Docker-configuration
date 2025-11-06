# CandyShop_AWS-Docker-configuration
Claro! Aqui está um **documento modelo** detalhado, explicativo e didático sobre o projeto de loja de doces ("Candy Shop") em AWS, com Docker, Flask, EC2, RDS, Lambda e API Gateway.

***

# **Candy Shop – Projeto Cloud AWS (2025)**

## **Visão Geral do Projeto**

O objetivo deste projeto é implementar uma arquitetura em nuvem para uma aplicação Flask de uma loja de doces ("Candy Shop"), totalmente containerizada com Docker, seguindo padrões modernos de cloud: separação de backend/frontend, banco gerenciado, utilização de Lambda Serverless e integração segura por API Gateway.  
O projeto busca demonstrar as melhores práticas em arquitetura cloud AWS distribuída, segurança de rede, automação e escalabilidade.

***

## **1. Desenvolvimento Local: App Flask + Docker**

### **1.1. Estrutura Básica do Projeto**
- Backend Python Flask: implementa API RESTful (rotas CRUD, `/report`, etc).
- Frontend web: pode ser Flask renderizando HTML ou client SPA chamando a API backend via HTTP.
- Repositório GitHub: organiza o código para backend e frontend de maneira independente.

### **1.2. Criação do Dockerfile**

**Exemplo para o backend Flask:**
```dockerfile
FROM python:3.10
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV FLASK_ENV=production
EXPOSE 25000
CMD ["flask", "run", "--host=0.0.0.0", "--port=25000"]
```
- Permite buildar o container onde for (dev, prod, AWS).
- Remova credenciais sensíveis, usando variáveis de ambiente para conectar ao banco.

### **1.3. Docker Compose**
Se desejar subir múltiplos containers juntos:
```yaml
version: "3"
services:
  backend:
    build: ./backend
    ports:
      - "25000:25000"
    environment:
      - DB_HOST=<rds_endpoint>
      - DB_USER=admin
      - DB_PASS=senha...
  frontend:
    build: ./frontend
    ports:
      - "8080:8080"
    environment:
      - BACKEND_HOST=<backend_private_ip>:25000
```

***

## **2. Infraestrutura AWS – Etapas e Justificativas**

### **2.1. Duas Instâncias EC2 Ubuntu**
- **Backend (privada):** responsável pela lógica e comunicação com o banco de dados. Em subnet privada, não acessível publicamente, reforçando segurança.
- **Frontend (pública):** expõe a aplicação web ao usuário final, única diretamente pública (porta 8080 aberta).

**Por quê?**  
Separar responsabilidades e proteger recursos sensíveis. O backend só se comunica com frontend/via VPC e banco, nunca é exposto publicamente — padrão para sistemas seguros.

**Passos realizados:**
- Escolha de AMI Ubuntu minimizando vulnerabilidades.
- Criação dos pares de chaves via AWS (SSH seguro).
- Grupos de segurança bem delimitados (porta 22 restrita, 25000 só entre front-back, 8080 aberto).

***

### **2.2. VPC, Sub-redes e Gateways**
- Criação de uma VPC exclusiva do projeto.
- Subrede pública (Frontend) com Internet Gateway — permite acesso externo.
- Subrede privada (Backend) sem Internet Gateway, apenas NAT para updates/se necessário.
- Roteamento e gatilhos configurados para garantir isolamento.

**Por quê?**  
Essencial para destacar recursos críticos (dados, lógica) do acesso público, evitar exposição.

***

### **2.3. Amazon RDS (MySQL)**
- Instância privada, só acessível pelo backend.
- Usuário e senha gerados/salvos na configuração do backend.
- Sem exposição pública, grupo de segurança permite acesso somente a `candyshop-backend-sg`.

**Por quê?**  
Banco gerenciado traz alta disponibilidade, backup, e elimina overhead operacional.

***

### **2.4. Deploy Docker nas EC2**
- SSH nas EC2, clone do GitHub.
- Build e run dos containers frontend/backend.
- Variáveis de ambiente exportadas antes ou direto no compose/run.

***

### **2.5. Lambda + API Gateway**
- Função Lambda em Python criada na mesma VPC, nas subredes privadas.
- Código Lambda consome o endpoint `/report` do backend por HTTP, via requests.
- API Gateway restaura padrão serverless/publicação RESTful seguro.
- Timeout da Lambda ajustado para 29 segundos, conforme o máximo suportado pela integração do API Gateway.

***

### **2.6. Segurança**
- Grupos de segurança delimitam cada papel e origem.
- Backend/banco nunca expostos publicamente.
- Lambda pode rodar restrita, autorizando apenas mínimo necessário.
- Frontend exposto apenas na porta 8080.

***

## **3. Passo a Passo para Rodar Tudo**

### **3.1. Backend (subnet privada)**
- SSH (via bastion/front ou Session Manager).
- `git clone` no backend/app.
- Build Docker.
- Export variáveis e run container.

### **3.2. Frontend (subnet pública)**
- SSH pela Internet.
- `git clone`, build e run Docker.
- Configure variáveis apontando para backend privado.

### **3.3. Lambda e API Gateway**
- Lambda criada/configurada no console AWS.
- Código da Lambda faz GET no API REST `/report` do backend (ajuste IP privado).
- API Gateway rota request externa `/report` para a função Lambda.
- Teste com browser/curl mostrando resposta JSON da API.

***

## **4. Checklist de Requisitos Atendidos**

- [x] Backend seguro, nunca público
- [x] Frontend acessível de fora
- [x] RDS privado
- [x] Lambda serverless e integração REST pelo Gateway
- [x] Rede segmentada, grupos de segurança restrictivos
- [x] Deploy totalmente Dockerizado (ambiente reproduzível!)
- [x] Documentação clara do fluxo

***

## **Considerações Finais e Oportunidades de Extensão**

- Você pode expandir usando pipelines CI/CD (GitHub Actions/AWS CodeBuild), adicionar monitoramento (CloudWatch), e publicar o repo/documentação para futuras turmas/projetos!

***

Se algum passo ficar vago ou se quiser detalhar um trecho específico (exemplo: comandos exatos de build/run Docker, diagrama visual, snippet do código Flask, variáveis de exemplo, logs/telas de segurança, explicações para leigos), me avise!  
Quanto mais informações personalizadas você quiser adicionar (como nomes reais de recursos, exemplos do app Flask ou prints), só dizer que ajusto o documento para a realidade do seu projeto.

[1](https://us-east-1.console.aws.amazon.com/ec2/home?region=us-east-1#Instances:)
