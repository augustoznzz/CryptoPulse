#!/usr/bin/env python3
"""
Test script para verificar se a análise de 30 moedas está funcionando
"""

from enhanced_analyzer import EnhancedCryptoAnalyzer
import time

def test_30_coins_analysis():
    """Testa se a análise de 30 moedas está funcionando corretamente"""
    print("🧪 Testando análise de 30 criptomoedas...")
    
    try:
        # Criar analisador
        analyzer = EnhancedCryptoAnalyzer(verbose=True)
        
        print("\n🔍 Executando análise das top 30 criptomoedas...")
        start_time = time.time()
        
        # Executar análise
        result = analyzer.find_best_opportunities(max_coins=30, top_results=5)
        
        analysis_time = time.time() - start_time
        
        if result.get('success'):
            opportunities = result.get('opportunities', [])
            total_analyzed = result.get('total_analyzed', 0)
            total_opportunities = result.get('total_opportunities', 0)
            
            print(f"\n✅ Análise concluída com sucesso!")
            print(f"📊 Tempo de análise: {analysis_time:.2f}s")
            print(f"🔍 Moedas analisadas: {total_analyzed}")
            print(f"🎯 Oportunidades encontradas: {total_opportunities}")
            print(f"🏆 Top 5 oportunidades retornadas: {len(opportunities)}")
            
            # Verificar se respeitou os limites
            if total_analyzed > 30:
                print(f"❌ ERRO: Analisou {total_analyzed} moedas, mas o limite era 30")
                return False
            else:
                print(f"✅ OK: Analisou {total_analyzed} moedas (limite: 30)")
            
            if len(opportunities) > 5:
                print(f"❌ ERRO: Retornou {len(opportunities)} oportunidades, mas o limite era 5")
                return False
            else:
                print(f"✅ OK: Retornou {len(opportunities)} oportunidades (limite: 5)")
            
            # Mostrar as oportunidades
            print(f"\n📈 Top {len(opportunities)} Oportunidades:")
            print("=" * 60)
            
            for i, signal in enumerate(opportunities, 1):
                formatted_signal = analyzer.format_signal_for_display(signal)
                if formatted_signal:
                    print(f"\n{i}. {formatted_signal['symbol']} - {formatted_signal['type']}")
                    print(f"   📊 Market Cap Rank: #{formatted_signal['market_cap_rank']}")
                    print(f"   📈 Potential Gain: {formatted_signal['potential_gain']:.2f}%")
                    print(f"   💪 Momentum Score: {formatted_signal['momentum_score']}")
                    print(f"   💰 Entry Price: ${formatted_signal['entry_price']:,.2f}")
                    print("-" * 40)
            
            print("\n✅ Teste de análise de 30 moedas concluído com sucesso!")
            return True
            
        else:
            print(f"❌ Erro na análise: {result.get('error', 'Erro desconhecido')}")
            return False
            
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_30_coins_analysis()
    if success:
        print("\n🎉 Análise de 30 moedas funcionando corretamente!")
    else:
        print("\n💥 Problema encontrado na análise de 30 moedas!") 