#!/usr/bin/env python3
"""
Script de teste para verificar a classificação de emails em português brasileiro
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.services.email_classifier import email_classifier
from app.utils.preprocessing import email_preprocessor

def test_portuguese_classification():
    """Testa a classificação de emails em português brasileiro"""
    
    print("Testando Classificação de Emails em Português Brasileiro")
    print("=" * 60)
    
    # Testes de emails produtivos
    productive_tests = [
        {
            "subject": "Problema urgente no sistema",
            "message": "Preciso de ajuda urgente com o sistema. Não consigo acessar meus dados e tenho uma reunião importante hoje.",
            "expected": "PRODUCTIVE"
        },
        {
            "subject": "Status do projeto XYZ",
            "message": "Preciso de uma atualização sobre o andamento do projeto XYZ. Quando será a próxima entrega?",
            "expected": "PRODUCTIVE"
        },
        {
            "subject": "Reunião de equipe amanhã",
            "message": "Lembrando que temos reunião de equipe amanhã às 14h. Por favor, preparem o relatório de atividades.",
            "expected": "PRODUCTIVE"
        },
        {
            "subject": "Erro no sistema de login",
            "message": "Estou enfrentando problemas para fazer login no sistema. O erro aparece sempre que tento acessar.",
            "expected": "PRODUCTIVE"
        },
        {
            "subject": "Solicitação de orçamento",
            "message": "Gostaria de solicitar um orçamento para o desenvolvimento do novo módulo. Preciso dos valores até sexta-feira.",
            "expected": "PRODUCTIVE"
        }
    ]
    
    # Testes de emails improdutivos
    unproductive_tests = [
        {
            "subject": "Parabéns pelo aniversário!",
            "message": "Parabéns pelo seu aniversário! Espero que tenha tido um dia maravilhoso. Um abraço!",
            "expected": "UNPRODUCTIVE"
        },
        {
            "subject": "Obrigado pela ajuda",
            "message": "Muito obrigado pela ajuda com o projeto. Você foi fundamental para o sucesso!",
            "expected": "UNPRODUCTIVE"
        },
        {
            "subject": "Convite para churrasco",
            "message": "E aí! Vamos fazer um churrasco no sábado? Traga a família!",
            "expected": "UNPRODUCTIVE"
        },
        {
            "subject": "Feliz aniversário!",
            "message": "Parabéns pelo seu aniversário! Espero que tenha um dia especial. Um abraço!",
            "expected": "UNPRODUCTIVE"
        },
        {
            "subject": "Newsletter da empresa",
            "message": "Confira as últimas notícias da nossa empresa. Novidades sobre produtos e serviços.",
            "expected": "UNPRODUCTIVE"
        }
    ]
    
    # Executar testes produtivos
    print("\nTestando Emails Produtivos:")
    print("-" * 40)
    
    productive_correct = 0
    for i, test in enumerate(productive_tests, 1):
        classification, response = email_classifier.classify_email(
            test["subject"], 
            test["message"]
        )
        
        is_correct = classification == test["expected"]
        if is_correct:
            productive_correct += 1
        
        status = "✅" if is_correct else "❌"
        print(f"{status} Teste {i}: {test['subject']}")
        print(f"   Classificação: {classification} (esperado: {test['expected']})")
        print(f"   Resposta: {response}")
        print()
    
    # Executar testes improdutivos
    print("\nTestando Emails Improdutivos:")
    print("-" * 40)
    
    unproductive_correct = 0
    for i, test in enumerate(unproductive_tests, 1):
        classification, response = email_classifier.classify_email(
            test["subject"], 
            test["message"]
        )
        
        is_correct = classification == test["expected"]
        if is_correct:
            unproductive_correct += 1
        
        status = "✅" if is_correct else "❌"
        print(f"{status} Teste {i}: {test['subject']}")
        print(f"   Classificação: {classification} (esperado: {test['expected']})")
        print(f"   Resposta: {response}")
        print()
    
    total_tests = len(productive_tests) + len(unproductive_tests)
    total_correct = productive_correct + unproductive_correct
    accuracy = (total_correct / total_tests) * 100
    
    print("Resultados:")
    print("=" * 40)
    print(f"Emails Produtivos: {productive_correct}/{len(productive_tests)} corretos")
    print(f"Emails Improdutivos: {unproductive_correct}/{len(unproductive_tests)} corretos")
    print(f"Total: {total_correct}/{total_tests} corretos")
    print(f"Precisão: {accuracy:.1f}%")
    
    if accuracy >= 80:
        print("Excelente! A classificação está funcionando bem.")
    elif accuracy >= 60:
        print("Bom! A classificação está funcionando, mas pode ser melhorada.")
    else:
        print("A classificação precisa de melhorias.")
    
    return accuracy

def test_preprocessing():
    """Testa o pré-processamento de texto em português"""
    
    print("\n🔧 Testando Pré-processamento de Texto:")
    print("=" * 50)
    
    test_texts = [
        "Preciso de ajuda URGENTE com o sistema!",
        "Obrigado pela sua mensagem. Agradeço muito!",
        "Reunião importante amanhã às 14h.",
        "Parabéns pelo seu aniversário!",
        "Problema crítico no banco de dados."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\nTeste {i}: {text}")
        
        cleaned = email_preprocessor.clean_text(text)
        print(f"   Limpo: {cleaned}")
        
        features = email_preprocessor.extract_features(text, "")
        print(f"   Features: {features}")
        
        is_productive = email_preprocessor.is_productive_keywords(text)
        is_unproductive = email_preprocessor.is_unproductive_keywords(text)
        print(f"   Produtivo: {is_productive}, Improdutivo: {is_unproductive}")

def main():
    """Função principal de teste"""
    try:
        test_preprocessing()
        
        accuracy = test_portuguese_classification()
        
        print(f"\nTeste concluído com {accuracy:.1f}% de precisão!")
        
        return 0 if accuracy >= 60 else 1
        
    except Exception as e:
        print(f"Erro durante o teste: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
