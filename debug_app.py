#!/usr/bin/env python3
"""
Debug script para identificar problemas na aplicação
"""

import requests
import json
import time

def test_api_directly():
    """Testa a API diretamente para identificar o problema"""
    print("🔍 Testando API diretamente...")
    
    try:
        # Teste 1: Verificar se o servidor está rodando
        print("1. Verificando se o servidor está rodando...")
        response = requests.get('http://localhost:5000/', timeout=5)
        print(f"   Status: {response.status_code}")
        
        # Teste 2: Testar a API de busca
        print("\n2. Testando API de busca...")
        response = requests.post(
            'http://localhost:5000/api/search-trades',
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Resposta: {json.dumps(data, indent=2)}")
        else:
            print(f"   Erro: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar ao servidor")
        print("   Certifique-se de que o servidor está rodando com: python app.py")
    except requests.exceptions.Timeout:
        print("❌ Erro: Timeout na requisição")
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")

def test_enhanced_analyzer():
    """Testa o EnhancedCryptoAnalyzer diretamente"""
    print("\n🔍 Testando EnhancedCryptoAnalyzer...")
    
    try:
        from enhanced_analyzer import EnhancedCryptoAnalyzer
        
        analyzer = EnhancedCryptoAnalyzer(verbose=True)
        
        # Teste simples
        print("   Testando busca de oportunidades...")
        result = analyzer.find_best_opportunities(max_coins=5, top_results=3)
        
        print(f"   Sucesso: {result.get('success', False)}")
        if result.get('success'):
            print(f"   Oportunidades encontradas: {len(result.get('opportunities', []))}")
        else:
            print(f"   Erro: {result.get('error', 'Erro desconhecido')}")
            
    except Exception as e:
        print(f"❌ Erro no EnhancedCryptoAnalyzer: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🚀 Iniciando debug da aplicação...")
    
    # Teste 1: EnhancedCryptoAnalyzer
    test_enhanced_analyzer()
    
    # Teste 2: API (se o servidor estiver rodando)
    print("\n" + "="*50)
    test_api_directly()
    
    print("\n✅ Debug concluído!") 