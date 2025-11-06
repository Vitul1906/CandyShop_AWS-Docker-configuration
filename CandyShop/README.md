
***

<div align="center">

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=2980B9&height=200&section=header&text=Doces%20Cloud&fontSize=50&fontColor=fff&animation=twinkling&fontAlignY=40&desc=AWS%20|%20Docker%20|%20Flask%20|%20EC2%20|%20VPC&descAlignY=60&descSize=18">

<p align="center">
  <i>🍬 Uma aplicação web elegante para gerenciar doces e pedidos, implantada em nuvem AWS usando containers Docker.</i>
</p>

***

### 📚 Projeto Acadêmico

<div align="center">

**Disciplina:** Serviços em Nuvem  
**Objetivo:** Familiarização com deploy de aplicações web com Docker e AWS EC2

</div>

### 🌟 Funcionalidades

<div align="center">

| Feature | Descrição |
|:---:|:---|
| 🍬 | Gerenciamento de Doces |
| 🧾 | Cadastro de Pedidos |
| 📊 | Relatórios e Estatísticas |
| 🌐 | API RESTful |
| 🐳 | Containers Docker |
| ☁️ | Deploy na Nuvem AWS |
| 🔒 | Isolamento seguro do backend |
| 🛡️ | Segurança de rede |

</div>

### 🛠️ Tecnologias

<div align="center">
  <a href="https://skillicons.dev">
    <img src="https://skillicons.dev/icons?i=python,flask,docker,aws,html,css,js&theme=dark" />
  </a>
</div>

### 🏗️ Arquitetura

```
┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │
│   (Porta 8080)  │◄──►│   (Porta 25000) │
│   Subrede Públ. │    │ Subrede Privada │
│   EC2 Instance  │    │  EC2 Instance   │
└─────────────────┘    └─────────────────┘
         │                        │
         ▼                        ▼
┌───────────────┐     ┌─────────────────┐
│   Internet    │     │   NAT Gateway   │
│   Gateway     │     │  (acesso temp.) │
└───────────────┘     └─────────────────┘
```

***

### 📋 Requisitos

- ✅ Interface web Flask responsiva
- ✅ Backend Flask API (CRUD de doces e pedidos)
- ✅ Dockerfiles para backend e frontend
- ✅ 2 EC2 (frontend pública, backend privada)
- ✅ VPC com subnets, rotas e grupos de segurança corretos
- ✅ Backend acessível só pelo frontend
- ✅ Portas: frontend (8080), backend (25000)
- ✅ Banco de dados RDS MySQL privado
- ✅ Função Lambda + API Gateway para estatísticas

***

### 🚀 Começando

#### Desenvolvimento Local

```bash
# Clone o projeto
git clone https://github.com/SEU_USUARIO/DocesCloudAWS.git
cd DocesCloudAWS

# Suba os serviços localmente
docker-compose up --build

# Acesse no navegador:
# Frontend: http://localhost:8080
# Backend API: http://localhost:25000/pedidos
```

#### Deploy AWS

**Backend (EC2 privada):**
```bash
sudo apt-get update
sudo apt-get install -y git docker.io
git clone https://github.com/SEU_USUARIO/DocesCloudAWS.git
cd DocesCloudAWS/backend
sudo docker build -t doces-backend-image .
sudo docker run -d --name backend \
  -e DB_HOST=<endpoint_rds> -e DB_USER=admin -e DB_PASS=suasenha \
  -p 25000:25000 doces-backend-image
```

**Frontend (EC2 pública):**
```bash
sudo apt-get update
sudo apt-get install -y git docker.io
git clone https://github.com/SEU_USUARIO/DocesCloudAWS.git
cd DocesCloudAWS/frontend
sudo docker build -t doces-frontend-image .
sudo docker run -d --name frontend \
  -e BACKEND_URL="http://<IP_PRIVADO_BACKEND>:25000" \
  -p 8080:8080 doces-frontend-image
```

***

### 📁 Estrutura do Projeto

```
DocesCloudAWS/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── app.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── static/
├── README.md
└── docker-compose.yml
```

***

### ☁️ Infraestrutura AWS

- **VPC:** Nuvem privada virtual customizada.
- **Subnets:** Pública (frontend) e privada (backend).
- **EC2:** t3.micro para cada função.
- **Security Groups:**  
   - Frontend: 8080 aberto à Internet, 22 restrito.  
   - Backend: 25000 aceitando conexões só do frontend.
- **RDS MySQL:** instância privada, SG permitindo acesso só do backend.  
- **Lambda/API Gateway:** para rota pública `/report`.

***

### 🛡️ Segurança

- Backend e banco SEM IP público.
- SG bem segmentados (acesso mínimo necessário).
- Lambda e API Gateway integrados só à API de estatística.
- SSH apenas por chave e limitado por IP.

***

### 🎯 Objetivos de Aprendizado

- [x] Containerização Docker e deploy cloud
- [x] Gestão, isolamento e roteamento AWS/VPC
- [x] Configuração avançada de segurança em cloud
- [x] Pipeline de deploy manual/controlado
- [x] Backend REST seguro
- [x] Integração Lambda serverless e exposição REST via API Gateway

***

### 📊 Endpoints da API

| Método | Endpoint       | Descrição                      |
|:------:|:-------------:|:-------------------------------|
| GET    | `/produtos`   | Lista os produtos              |
| POST   | `/pedidos`    | Cria um novo pedido            |
| GET    | `/report`     | Retorna relatório/estatística  |

***

### 👣 Passo a passo do projeto (com explicações)

1. **Desenvolvimento local**:  
   - Criamos o app Flask para frontend e backend.
   - Utilizamos Docker para garantir portabilidade e isolamento do ambiente (basta rodar `docker-compose` para simular localmente).

2. **Planejamento e criação da infraestrutura AWS**:  
   - Definimos uma VPC exclusiva, com subredes pública (frontend) e privada (backend).
   - Criamos as instâncias EC2 conforme papel (pública e privada).
   - Configuramos grupos de segurança para garantir acesso mínimo entre instâncias e abrir apenas o necessário para acesso do usuário final.

3. **Banco de dados**:  
   - Implantação de uma instância Amazon RDS MySQL privada, acessível somente pela EC2 backend.
   - Garantia de segurança dos dados por isolamento de rede e regras de SG.

4. **Deploy das aplicações**:  
   - Clonamos o repositório nas EC2, buildamos as imagens Docker e rodamos containers em cada serviço.
   - Backend comunica-se com RDS via variáveis de ambiente, frontend acessa backend por IP privado da VPC.

5. **Configuração Lambda e API Gateway**:  
   - Lambda criada em Python para consumir o endpoint `/report` do backend.
   - API Gateway expõe rota `/report` para consumo público seguro.
   - Timeout ajustado conforme o esperado para resposta completa.

6. **Testes e validação**:  
   - Garantimos que cada camada responde apropriadamente, endpoints seguros e recursos nunca expostos desnecessariamente.
   - Avaliação da arquitetura, logs, e cumprimento dos requisitos acadêmicos.

***

### 👤 Autor

<div align="center">
  <a href="https://github.com/SEU_USUARIO" target="_blank">
    <img src="https://skillicons.dev/icons?i=github" alt="GitHub"/>
  </a>
</div>

### 📜 Licença

Projeto sob licença MIT – veja o arquivo [LICENSE](LICENSE) para mais detalhes.

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&color=2980B9&height=120&section=footer"/>

</div>

***
