#!/usr/bin/env python3
"""
Script de teste para verificar se a API está funcionando corretamente
"""

import requests
import json
import sys

# Configuração
BASE_URL = "http://localhost:8000"
GRAPHQL_URL = f"{BASE_URL}/graphql"

def test_health_check():
    """Testa o endpoint de health check"""
    print("Testando health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("Health check OK")
            return True
        else:
            print(f"Health check falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"Erro no health check: {e}")
        return False

def test_graphql_endpoint():
    """Testa se o endpoint GraphQL está respondendo"""
    print("Testando endpoint GraphQL...")
    try:
        query = """
        query {
            __schema {
                types {
                    name
                }
            }
        }
        """
        
        response = requests.post(
            GRAPHQL_URL,
            json={"query": query},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            print("Endpoint GraphQL OK")
            return True
        else:
            print(f"Endpoint GraphQL falhou: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
    except Exception as e:
        print(f"Erro no endpoint GraphQL: {e}")
        return False

def test_login_mutation():
    """Testa a mutation de login"""
    print("Testando mutation de login...")
    try:
        mutation = """
        mutation {
            login(input: {
                email: "test@example.com"
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
        """
        
        response = requests.post(
            GRAPHQL_URL,
            json={"query": mutation},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print(f"Login falhou (esperado se usuário não existir): {data['errors']}")
            else:
                print("Login mutation OK")
            return True
        else:
            print(f"Login mutation falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"Erro na mutation de login: {e}")
        return False

def test_create_user_mutation():
    """Testa a mutation de criação de usuário"""
    print("Testando mutation de criação de usuário...")
    try:
        mutation = """
        mutation {
            createUserAccount(input: {
                name: "Usuário Teste"
                email: "teste@example.com"
                password: "senha123"
            }) {
                id
                name
                email
            }
        }
        """
        
        response = requests.post(
            GRAPHQL_URL,
            json={"query": mutation},
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                print(f"Criação de usuário falhou: {data['errors']}")
            else:
                print("Criação de usuário OK")
            return True
        else:
            print(f"Criação de usuário falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f"Erro na criação de usuário: {e}")
        return False

def main():
    """Função principal de teste"""
    print("Iniciando testes da API...")
    print(f"URL base: {BASE_URL}")
    print(f"GraphQL URL: {GRAPHQL_URL}")
    print("-" * 50)
    
    tests = [
        test_health_check,
        test_graphql_endpoint,
        test_create_user_mutation,
        test_login_mutation,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("Todos os testes passaram!")
        return 0
    else:
        print("Alguns testes falharam. Verifique os logs acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
