# Seleciona AI Backend

Sistema de classificação de emails em categorias produtivas e improdutivas usando Python, FastAPI, GraphQL e IA.

- **Observações**: O ML principal utilizado no projeto não está com acurácia satisfatória e a classificação baseada em regras está mais precisa. Configure a variável USE_ML_MODEL no .env para False para usar classificação baseada em regras e True para utilizar modelos de linguagem.

## Funcionalidades

- **Autenticação JWT**: Sistema completo de autenticação com tokens JWT
- **Classificação de Emails**: Análise automática de emails usando NLP e IA em português brasileiro
- **API GraphQL**: Interface GraphQL completa com queries e mutations
- **Banco de Dados MySQL**: Persistência de dados com SQLAlchemy
- **Upload de Arquivos**: Processamento de imagens e documentos
- **Estatísticas**: Relatórios de produtividade dos emails
- **Suporte PT-BR**: Classificação otimizada para português brasileiro

## Suporte ao Português Brasileiro

O sistema foi especialmente otimizado para classificar emails em português brasileiro, incluindo: 

### Palavras-chave Produtivas
- **Urgência**: urgente, urgência, asap, prazo, deadline, hoje, amanhã
- **Reuniões**: reunião, meeting, encontro, agendamento, compromisso
- **Projetos**: projeto, tarefa, atividade, trabalho, entrega
- **Problemas**: problema, erro, bug, falha, corrigir, resolver
- **Negócios**: cliente, venda, contrato, proposta, orçamento

### Palavras-chave Improdutivas
- **Agradecimentos**: obrigado, obrigada, parabéns, felicitações
- **Datas especiais**: aniversário, natal, páscoa, feriado
- **Convites sociais**: convite, evento, churrasco, festa
- **Spam**: publicidade, promoção, oferta, marketing
- **Pessoal**: família, amigos, vida pessoal, particular

### Modelo de IA
- **Modelo principal**: `neuralmind/bert-base-portuguese-cased`
- **Modelo fallback**: `distilbert-base-multilingual-cased`
- **Classificação baseada em regras**: Para casos onde o modelo de IA não está disponível

### Respostas Automáticas
- **Produtivas**: "Obrigado pelo seu email sobre '{subject}'. Vou analisar e retornar em breve."
- **Improdutivas**: "Obrigado pela sua mensagem. Agradeço por pensar em mim."

## Tecnologias Utilizadas

- **Strawberry GraphQL**: Implementação GraphQL para Python
- **SQLAlchemy**: ORM para banco de dados
- **Alembic**: Migrações de banco de dados
- **MySQL**: Banco de dados relacional
- **JWT**: Autenticação baseada em tokens
- **Transformers**: Modelos de IA para classificação de texto
- **NLTK**: Processamento de linguagem natural

## Instalação

### 1. Pré-requisitos

- Python 3.8+
- MySQL 5.7+
- pip (gerenciador de pacotes Python)

### 2. Clone o repositório

```bash
git clone <repository-url>
cd seleciona-ai/backend
```

### 3. Crie um ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Instale as dependências

```bash
pip install -r requirements.txt
```

### 5. Configure o banco de dados

1. Crie um banco de dados MySQL:
```sql
CREATE DATABASE seleciona_ai_db;
CREATE USER 'seleciona_user'@'localhost' IDENTIFIED BY 'seleciona_password';
GRANT ALL PRIVILEGES ON seleciona_ai_db.* TO 'seleciona_user'@'localhost';
FLUSH PRIVILEGES;
```

2. Configure as variáveis de ambiente:
```bash
# Copie o arquivo de exemplo
cp env.example .env

# Edite o arquivo .env com suas configurações
```

3. Execute as migrações:
```bash
alembic upgrade head
```

### 6. Configure as variáveis de ambiente

Edite o arquivo `.env` com suas configurações:

```env
# Database Configuration
DATABASE_URL=mysql+pymysql://seleciona_user:seleciona_password@localhost:3306/seleciona_ai_db

# JWT Configuration
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# File Upload Configuration
UPLOAD_DIR=uploads
MAX_FILE_SIZE=2097152  # 2MB in bytes
ALLOWED_IMAGE_EXTENSIONS=jpg,jpeg,png,webp
ALLOWED_DOCUMENT_EXTENSIONS=txt,pdf

# AI Configuration
HUGGINGFACE_API_KEY=your-huggingface-api-key-here
MODEL_NAME=neuralmind/bert-base-portuguese-cased

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# ML Model Toggle - Set to False to use rule-based classification only
USE_ML_MODEL=False
```

## Executando a aplicação

### Desenvolvimento

```bash
python main.py
```

### Produção

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

A aplicação estará disponível em:
- **API**: http://localhost:8000
- **GraphQL Playground**: http://localhost:8000/graphql
- **Documentação**: http://localhost:8000/docs

## Estrutura do Projeto

```
backend/
├── app/
│   ├── models/              # Modelos do banco de dados
│   │   ├── user.py
│   │   ├── categorized_email.py
│   │   └── email_statistics.py
│   ├── schemas/             # Schemas GraphQL
│   │   ├── user.py
│   │   ├── email.py
│   │   ├── statistics.py
│   │   └── auth.py
│   ├── resolvers/           # Resolvers GraphQL
│   │   ├── queries.py
│   │   └── mutations.py
│   ├── services/            # Lógica de negócio
│   │   ├── user_service.py
│   │   └── email_service.py
│   ├── utils/               # Utilitários
│   │   └── preprocessing.py
│   ├── migrations/          # Migrações do banco
│   ├── config.py            # Configurações
│   ├── database.py          # Configuração do banco
│   └── auth.py              # Autenticação
├── uploads/                 # Arquivos enviados
├── main.py                  # Aplicação principal
├── requirements.txt         # Dependências
├── alembic.ini             # Configuração do Alembic
└── README.md               # Este arquivo
```

## API GraphQL

### Queries

- `getUser`: Retorna dados do usuário logado
- `getStatistics`: Retorna estatísticas dos emails
- `getEmailsList`: Lista emails com paginação
- `getEmail`: Retorna um email específico

### Mutations

- `login`: Autenticação do usuário
- `createUserAccount`: Criar nova conta
- `updateUserAccount`: Atualizar conta do usuário
- `analyseEmail`: Analisar um email individual
- `analyseEmails`: Analisar múltiplos emails de arquivo
- `updateEmail`: Atualizar resposta do email
- `deleteEmail`: Excluir email

## Exemplos de Uso

### 1. Login

```graphql
mutation {
  login(input: {
    email: "user@example.com"
    password: "password123"
  }) {
    token
    user {
      id
      name
      email
    }
  }
}
```

### 2. Analisar Email (Português Brasileiro)

```graphql
mutation {
  analyseEmail(input: {
    email: "cliente@empresa.com"
    subject: "Problema urgente no sistema"
    message: "Preciso de ajuda urgente com o sistema. Não consigo acessar meus dados e tenho uma reunião importante hoje."
  }) {
    id
    classification
    response
  }
}
```

**Resposta:**
```json
{
  "data": {
    "analyseEmail": {
      "id": 1,
      "classification": "PRODUCTIVE",
      "response": "Obrigado pelo seu email sobre 'Problema urgente no sistema'. Vou analisar e retornar em breve."
    }
  }
}
```

### 3. Listar Emails

```graphql
query {
  getEmailsList(page: 1, perPage: 10) {
    emails {
      id
      subject
      classification
      createdAt
    }
    pagination {
      total
      totalPages
    }
  }
}
```

### Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-asyncio

# Executar testes
pytest
```

### Teste Geral da API
```bash
python test_api.py
```

### Teste de Classificação em Português
```bash
python test_portuguese_classification.py
```

Este teste verifica:
- Classificação de emails produtivos em português
- Classificação de emails improdutivos em português
- Pré-processamento de texto em português
- Precisão da classificação

### Exemplos de Teste
O arquivo `examples/api_examples_pt.md` contém exemplos completos de uso da API com emails em português brasileiro.

## Comandos Úteis

### Usando Makefile

```bash
# Ver todos os comandos disponíveis
make help

# Instalar dependências
make install

# Executar em modo desenvolvimento
make dev

# Executar em modo produção
make prod

# Executar testes
make test

# Executar migrações
make migrate

# Limpar arquivos temporários
make clean
```

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
