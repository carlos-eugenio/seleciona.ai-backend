# Exemplos de Uso da API

Este documento contém exemplos práticos de como usar a API GraphQL do Seleciona AI Backend.

## Configuração Inicial

### 1. Criar Usuário

```graphql
mutation {
  createUserAccount(input: {
    name: "João Silva"
    email: "joao@example.com"
    password: "senha123"
  }) {
    id
    name
    email
  }
}
```

### 2. Login

```graphql
mutation {
  login(input: {
    email: "joao@example.com"
    password: "senha123"
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

**Resposta:**
```json
{
  "data": {
    "login": {
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "user": {
        "id": 1,
        "name": "João Silva",
        "email": "joao@example.com"
      }
    }
  }
}
```

## Análise de Emails

### 1. Analisar Email Individual (Produtivo)

```graphql
mutation {
  analyseEmail(input: {
    email: "cliente@empresa.com"
    subject: "Problema urgente no sistema"
    message: "Preciso de ajuda urgente com o sistema. Não consigo acessar meus dados e tenho uma reunião importante hoje."
  }) {
    id
    email
    subject
    classification
    response
    createdAt
  }
}
```

**Resposta:**
```json
{
  "data": {
    "analyseEmail": {
      "id": 1,
      "email": "cliente@empresa.com",
      "subject": "Problema urgente no sistema",
      "classification": "PRODUCTIVE",
      "response": "Obrigado pelo seu email sobre 'Problema urgente no sistema'. Vou analisar e retornar em breve.",
      "createdAt": "2024-01-15T10:30:00Z"
    }
  }
}
```

### 2. Analisar Email Improdutivo

### 3. Mais Exemplos de Emails Produtivos

```graphql
# Email sobre projeto
mutation {
  analyseEmail(input: {
    email: "gerente@empresa.com"
    subject: "Status do projeto XYZ"
    message: "Preciso de uma atualização sobre o andamento do projeto XYZ. Quando será a próxima entrega?"
  }) {
    classification
    response
  }
}

# Email sobre reunião
mutation {
  analyseEmail(input: {
    email: "colaborador@empresa.com"
    subject: "Reunião de equipe amanhã"
    message: "Lembrando que temos reunião de equipe amanhã às 14h. Por favor, preparem o relatório de atividades."
  }) {
    classification
    response
  }
}

# Email sobre problema técnico
mutation {
  analyseEmail(input: {
    email: "suporte@empresa.com"
    subject: "Erro no sistema de login"
    message: "Estou enfrentando problemas para fazer login no sistema. O erro aparece sempre que tento acessar."
  }) {
    classification
    response
  }
}
```

### 4. Mais Exemplos de Emails Improdutivos

```graphql
# Email de agradecimento
mutation {
  analyseEmail(input: {
    email: "colega@empresa.com"
    subject: "Obrigado pela ajuda"
    message: "Muito obrigado pela ajuda com o projeto. Você foi fundamental para o sucesso!"
  }) {
    classification
    response
  }
}

# Email de aniversário
mutation {
  analyseEmail(input: {
    email: "amigo@email.com"
    subject: "Feliz aniversário!"
    message: "Parabéns pelo seu aniversário! Espero que tenha um dia especial. Um abraço!"
  }) {
    classification
    response
  }
}

# Email de convite social
mutation {
  analyseEmail(input: {
    email: "amigo@email.com"
    subject: "Convite para churrasco"
    message: "E aí! Vamos fazer um churrasco no sábado? Traga a família!"
  }) {
    classification
    response
  }
}

```graphql
mutation {
  analyseEmail(input: {
    email: "amigo@email.com"
    subject: "Parabéns pelo aniversário!"
    message: "Parabéns pelo seu aniversário! Espero que tenha tido um dia maravilhoso. Um abraço!"
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
      "id": 2,
      "classification": "UNPRODUCTIVE",
      "response": "Obrigado pela sua mensagem. Agradeço por pensar em mim."
    }
  }
}
```

## Consultas de Dados

### 1. Obter Dados do Usuário

```graphql
query {
  getUser {
    id
    name
    email
    avatarUrl
    avatarThumbnailUrl
  }
}
```

### 2. Listar Emails com Paginação

```graphql
query {
  getEmailsList(page: 1, perPage: 5) {
    emails {
      id
      email
      subject
      classification
      createdAt
    }
    pagination {
      page
      perPage
      total
      totalPages
    }
  }
}
```

### 3. Obter Email Específico

```graphql
query {
  getEmail(emailId: 1) {
    id
    email
    subject
    response
    classification
    createdAt
    updatedAt
  }
}
```

### 4. Obter Estatísticas

```graphql
query {
  getStatistics {
    id
    total
    productive
    unproductive
    percentageProductive
    percentageUnproductive
  }
}
```

**Resposta:**
```json
{
  "data": {
    "getStatistics": {
      "id": 1,
      "total": 10,
      "productive": 7,
      "unproductive": 3,
      "percentageProductive": 70.0,
      "percentageUnproductive": 30.0
    }
  }
}
```

## Gerenciamento de Emails

### 1. Atualizar Resposta do Email

```graphql
mutation {
  updateEmail(input: {
    emailId: 1
    response: "Obrigado pelo contato. Vou verificar o problema e retornar em breve com uma solução."
  }) {
    id
    response
    updatedAt
  }
}
```

### 2. Excluir Email

```graphql
mutation {
  deleteEmail(emailId: 1)
}
```

**Resposta:**
```json
{
  "data": {
    "deleteEmail": true
  }
}
```

## Gerenciamento de Usuário

### 1. Atualizar Conta do Usuário

```graphql
mutation {
  updateUserAccount(input: {
    name: "João Silva Santos"
    email: "joao.silva@example.com"
  }) {
    id
    name
    email
  }
}
```

## Headers de Autenticação

Para todas as operações (exceto login e createUserAccount), inclua o header de autorização:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Exemplo com cURL

### Login

```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { login(input: { email: \"joao@example.com\", password: \"senha123\" }) { token user { id name email } } }"
  }'
```

### Analisar Email

```bash
curl -X POST http://localhost:8000/graphql \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -d '{
    "query": "mutation { analyseEmail(input: { email: \"teste@example.com\", subject: \"Teste\", message: \"Mensagem de teste\" }) { id classification response } }"
  }'
```

## Códigos de Erro Comuns

### 401 Unauthorized
```json
{
  "errors": [
    {
      "message": "Authentication required",
      "extensions": {
        "code": "UNAUTHENTICATED"
      }
    }
  ]
}
```

### 400 Bad Request
```json
{
  "errors": [
    {
      "message": "Invalid email or password",
      "extensions": {
        "code": "BAD_REQUEST"
      }
    }
  ]
}
```

### 404 Not Found
```json
{
  "errors": [
    {
      "message": "Email not found",
      "extensions": {
        "code": "NOT_FOUND"
      }
    }
  ]
}
```

## Testando no GraphQL Playground

1. Acesse http://localhost:8000/graphql
2. Use o painel de consultas para testar as queries e mutations
3. Configure os headers de autorização no painel inferior
4. Explore a documentação interativa no painel direito
