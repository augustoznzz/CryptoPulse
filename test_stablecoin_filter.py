#!/usr/bin/env python3
"""
Test script para verificar a exclusão de stablecoins
"""

from market_data import MarketDataFetcher
from enhanced_analyzer import EnhancedCryptoAnalyzer
import time

def test_stablecoin_filter():
    """Testa se stablecoins estão sendo filtradas corretamente"""
    print("🧪 Testando filtro de stablecoins...")
    
    try:
        # Teste 1: Verificar se stablecoins são filtradas no MarketDataFetcher
        print("\n1. Testando filtro no MarketDataFetcher...")
        market_fetcher = MarketDataFetcher(verbose=True)
        
        # Buscar top 20 criptomoedas
        top_coins = market_fetcher.get_top_cryptocurrencies(limit=20)
        
        print(f"   Total de moedas encontradas: {len(top_coins)}")
        
        # Verificar quais são stablecoins
        stablecoins_found = []
        for coin in top_coins:
            symbol = coin.get('symbol', '').upper()
            if symbol in ['USDT', 'USDC', 'BUSD', 'DAI', 'TUSD', 'USDP', 'USDD', 'FRAX', 'STETH', 'WSTETH', 'WEETH', 'WBETH', 'BSC-USD']:
                stablecoins_found.append(symbol)
        
        print(f"   Stablecoins encontradas: {stablecoins_found}")
        
        # Aplicar filtro
        filtered_coins = market_fetcher.filter_by_technical_criteria(top_coins)
        
        print(f"   Moedas após filtro: {len(filtered_coins)}")
        
        # Verificar se stablecoins foram removidas
        remaining_stablecoins = []
        for coin in filtered_coins:
            symbol = coin.get('symbol', '').upper()
            if symbol in ['USDT', 'USDC', 'BUSD', 'DAI', 'TUSD', 'USDP', 'USDD', 'FRAX', 'STETH', 'WSTETH', 'WEETH', 'WBETH', 'BSC-USD']:
                remaining_stablecoins.append(symbol)
        
        if remaining_stablecoins:
            print(f"   ❌ ERRO: Stablecoins ainda presentes após filtro: {remaining_stablecoins}")
            return False
        else:
            print("   ✅ Stablecoins foram filtradas corretamente")
        
        # Teste 2: Verificar se stablecoins são filtradas no EnhancedCryptoAnalyzer
        print("\n2. Testando filtro no EnhancedCryptoAnalyzer...")
        analyzer = EnhancedCryptoAnalyzer(verbose=True)
        
        # Teste com poucas moedas para velocidade
        result = analyzer.find_best_opportunities(max_coins=10, top_results=5)
        
        if result.get('success'):
            opportunities = result.get('opportunities', [])
            print(f"   Oportunidades encontradas: {len(opportunities)}")
            
            # Verificar se há stablecoins nas oportunidades
            stablecoins_in_opportunities = []
            for opp in opportunities:
                symbol = opp.get('symbol', '').upper()
                if symbol in ['USDT', 'USDC', 'BUSD', 'DAI', 'TUSD', 'USDP', 'USDD', 'FRAX', 'STETH', 'WSTETH', 'WEETH', 'WBETH', 'BSC-USD']:
                    stablecoins_in_opportunities.append(symbol)
            
            if stablecoins_in_opportunities:
                print(f"   ❌ ERRO: Stablecoins nas oportunidades: {stablecoins_in_opportunities}")
                return False
            else:
                print("   ✅ Nenhuma stablecoin encontrada nas oportunidades")
                
            # Mostrar algumas oportunidades
            print("\n   📊 Primeiras oportunidades:")
            for i, opp in enumerate(opportunities[:3], 1):
                symbol = opp.get('symbol', 'Unknown')
                signal_type = opp.get('type', 'Unknown')
                print(f"   {i}. {symbol} - {signal_type}")
        else:
            print(f"   ❌ Erro na análise: {result.get('error', 'Erro desconhecido')}")
            return False
        
        print("\n✅ Teste de filtro de stablecoins concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_stablecoin_filter()
    if success:
        print("\n🎉 Filtro de stablecoins funcionando corretamente!")
    else:
        print("\n💥 Problema encontrado no filtro de stablecoins!") 