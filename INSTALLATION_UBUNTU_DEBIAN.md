# Instalação no Ubuntu/Debian - Seleciona AI Backend

## Pré-requisitos

### 1. Atualizar o sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Python 3.8+

```bash
# Verificar se Python já está instalado
python3 --version

# Se não estiver instalado ou for versão antiga:
sudo apt install python3 python3-pip python3-venv python3-dev -y

# Verificar instalação
python3 --version
pip3 --version
```

### 3. Instalar MySQL

```bash
# Instalar MySQL Server
sudo apt install mysql-server -y

# Iniciar e habilitar MySQL
sudo systemctl start mysql
sudo systemctl enable mysql

# Configurar MySQL (opcional - para definir senha do root)
sudo mysql_secure_installation
```

### 4. Instalar dependências do sistema

```bash
# Dependências necessárias para compilar alguns pacotes Python
sudo apt install build-essential libssl-dev libffi-dev libmysqlclient-dev pkg-config -y
```

### 5. Instalar Git (se não estiver instalado)

```bash
sudo apt install git -y
```

## Instalação do Projeto

### 1. Navegar para o diretório do projeto

```bash
cd /path/to/seleciona-ai/backend
```

### 2. Criar ambiente virtual

```bash
python3 -m venv venv
```

### 3. Ativar ambiente virtual

```bash
source venv/bin/activate
```

### 4. Atualizar pip

```bash
python -m pip install --upgrade pip
```

### 5. Instalar dependências

```bash
pip install -r requirements.txt
```

### 6. Configurar banco de dados

```bash
# Conectar ao MySQL como root
sudo mysql

# No prompt do MySQL, execute:
CREATE DATABASE seleciona_ai_db;
CREATE USER 'seleciona_user'@'localhost' IDENTIFIED BY 'seleciona_password';
GRANT ALL PRIVILEGES ON seleciona_ai_db.* TO 'seleciona_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 7. Configurar variáveis de ambiente

```bash
# Copiar arquivo de exemplo
cp env.example .env
```

#### Editar arquivo .env:
```bash
# Editar arquivo .env
nano .env

# Conteúdo para MySQL:
DATABASE_URL=mysql+pymysql://seleciona_user:seleciona_password@localhost:3306/seleciona_ai_db
SECRET_KEY=sua-chave-secreta-aqui-mude-em-producao
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
UPLOAD_DIR=uploads
MAX_FILE_SIZE=2097152
ALLOWED_IMAGE_EXTENSIONS=jpg,jpeg,png,webp
ALLOWED_DOCUMENT_EXTENSIONS=txt,pdf
HUGGINGFACE_API_KEY=your-huggingface-api-key-here-optional
MODEL_NAME=neuralmind/bert-base-portuguese-cased
HOST=0.0.0.0
PORT=8000
DEBUG=True
USE_ML_MODEL=False
```

### 8. Executar migrações

```bash
# Certificar que o ambiente virtual está ativo
source venv/bin/activate

# Executar migrações
alembic upgrade head
```

### 9. Executar a aplicação

```bash
# Modo desenvolvimento
python main.py

# Ou usando uvicorn diretamente
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## Verificação da Instalação

### 1. Testar se a aplicação está rodando

Abra o navegador e acesse:
- http://localhost:8000 (página inicial)
- http://localhost:8000/graphql (GraphQL Playground)
- http://localhost:8000/docs (Documentação da API)

### 2. Executar testes

```bash
# Teste geral da API
python test_api.py

# Teste de classificação em português
python test_portuguese_classification.py
```

## Comandos Úteis

### Ativar ambiente virtual
```bash
source venv/bin/activate
```

### Desativar ambiente virtual
```bash
deactivate
```

### Executar migrações
```bash
alembic upgrade head
```

## Usando Makefile

O projeto inclui um Makefile com comandos úteis:

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

## Estrutura de Arquivos

```
backend/
├── app/                    # Código da aplicação
│   ├── models/            # Modelos do banco de dados
│   ├── schemas/           # Schemas GraphQL
│   ├── resolvers/         # Resolvers GraphQL
│   ├── services/          # Lógica de negócio
│   ├── utils/             # Utilitários
│   └── migrations/        # Migrações do banco
├── uploads/               # Arquivos enviados
├── venv/                  # Ambiente virtual
├── main.py               # Arquivo principal
├── requirements.txt      # Dependências
├── .env                  # Variáveis de ambiente
├── alembic.ini          # Configuração do Alembic
├── Makefile             # Comandos úteis
└── README.md            # Documentação
```


