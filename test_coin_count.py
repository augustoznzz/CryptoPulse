#!/usr/bin/env python3
"""
Test script para verificar se a quantidade de moedas está sendo respeitada
"""

from enhanced_analyzer import EnhancedCryptoAnalyzer
from market_data import MarketDataFetcher
import time

def test_coin_count():
    """Testa se a quantidade de moedas está sendo respeitada"""
    print("🧪 Testando quantidade de moedas...")
    
    try:
        # Teste 1: Verificar se o MarketDataFetcher respeita o limite
        print("\n1. Testando MarketDataFetcher...")
        market_fetcher = MarketDataFetcher(verbose=True)
        
        # Testar diferentes limites
        test_limits = [10, 20, 30]
        
        for limit in test_limits:
            print(f"\n   Testando limite: {limit}")
            coins = market_fetcher.get_top_cryptocurrencies(limit=limit)
            print(f"   Moedas retornadas: {len(coins)}")
            
            if len(coins) > limit:
                print(f"   ❌ ERRO: Retornou {len(coins)} moedas, mas o limite era {limit}")
                return False
            else:
                print(f"   ✅ OK: Retornou {len(coins)} moedas (limite: {limit})")
        
        # Teste 2: Verificar se o EnhancedCryptoAnalyzer respeita o max_coins
        print("\n2. Testando EnhancedCryptoAnalyzer...")
        analyzer = EnhancedCryptoAnalyzer(verbose=True)
        
        # Testar diferentes valores de max_coins
        test_max_coins = [5, 10, 15]
        
        for max_coins in test_max_coins:
            print(f"\n   Testando max_coins: {max_coins}")
            result = analyzer.find_best_opportunities(max_coins=max_coins, top_results=3)
            
            if result.get('success'):
                total_analyzed = result.get('total_analyzed', 0)
                print(f"   Moedas analisadas: {total_analyzed}")
                
                if total_analyzed > max_coins:
                    print(f"   ❌ ERRO: Analisou {total_analyzed} moedas, mas o limite era {max_coins}")
                    return False
                else:
                    print(f"   ✅ OK: Analisou {total_analyzed} moedas (limite: {max_coins})")
                    
                # Mostrar algumas oportunidades
                opportunities = result.get('opportunities', [])
                print(f"   Oportunidades encontradas: {len(opportunities)}")
                
                for i, opp in enumerate(opportunities[:2], 1):
                    symbol = opp.get('symbol', 'Unknown')
                    signal_type = opp.get('type', 'Unknown')
                    print(f"   {i}. {symbol} - {signal_type}")
            else:
                print(f"   ❌ Erro na análise: {result.get('error', 'Erro desconhecido')}")
                return False
        
        print("\n✅ Teste de quantidade de moedas concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_coin_count()
    if success:
        print("\n🎉 Quantidade de moedas sendo respeitada corretamente!")
    else:
        print("\n💥 Problema encontrado na quantidade de moedas!") 