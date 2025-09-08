#!/usr/bin/env python3
"""
Script de configuração inicial do projeto Seleciona AI Backend
"""

import os
import subprocess
import sys

def run_command(command, description):
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"{description} - Sucesso!")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description} - Erro!")
        print(f"Erro: {e.stderr}")
        return False

def create_env_file():
    if not os.path.exists('.env'):
        if os.path.exists('.env.example'):
            print("Criando arquivo .env...")
            with open('.env.example', 'r') as src:
                content = src.read()
            with open('.env', 'w') as dst:
                dst.write(content)
            print("Arquivo .env criado! Lembre-se de configurar as variáveis.")
        else:
            print("Arquivo .env.example não encontrado!")
            return False
    else:
        print("Arquivo .env já existe.")
    return True

def main():
    print("Configurando Seleciona AI Backend...")
    
    if sys.version_info < (3, 8):
        print("Python 3.8+ é necessário!")
        sys.exit(1)
    
    print(f"Python {sys.version.split()[0]} detectado")
    
    if not create_env_file():
        sys.exit(1)
    
    if not run_command("pip install -r requirements.txt", "Instalando dependências"):
        print("Falha ao instalar dependências!")
        sys.exit(1)
    
    directories = ["uploads", "uploads/avatars", "app/migrations/versions"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Diretório {directory} criado/verificado")
    
    print("\nConfiguração concluída!")
    print("\nPróximos passos:")
    print("1. Configure o arquivo .env com suas credenciais do banco de dados")
    print("2. Crie o banco de dados MySQL: CREATE DATABASE seleciona_ai_db;")
    print("3. Execute as migrações: alembic upgrade head")
    print("4. Execute a aplicação: python main.py")
    print("\nA aplicação estará disponível em: http://localhost:8000")
    print("GraphQL Playground: http://localhost:8000/graphql")

if __name__ == "__main__":
    main()
