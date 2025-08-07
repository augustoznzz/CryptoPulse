#!/usr/bin/env python3
"""
Test script para verificar os novos indicadores
"""

from technical_indicators import TechnicalIndicators
from market_data import MarketDataFetcher
import pandas as pd
import numpy as np

def test_new_indicators():
    """Testa os novos indicadores de volume e Fibonacci"""
    print("🧪 Testando novos indicadores...")
    
    try:
        # Criar dados de exemplo
        dates = pd.date_range('2024-01-01', periods=100, freq='D')
        np.random.seed(42)
        
        # Gerar dados OHLCV realistas
        base_price = 100
        prices = []
        volumes = []
        
        price_history = []
        for i in range(100):
            # Simular movimento de preço
            if i == 0:
                price = base_price
            else:
                change = np.random.normal(0, 0.02)  # 2% volatilidade diária
                price = price_history[-1] * (1 + change)
            
            price_history.append(price)
            
            # Gerar OHLC
            high = price * (1 + abs(np.random.normal(0, 0.01)))
            low = price * (1 - abs(np.random.normal(0, 0.01)))
            open_price = price * (1 + np.random.normal(0, 0.005))
            close = price
            
            # Gerar volume com tendência
            base_volume = 1000000
            volume_trend = 1 + (i / 100) * 0.5  # Tendência crescente
            volume = base_volume * volume_trend * (1 + np.random.normal(0, 0.3))
            
            prices.append({
                'open': open_price,
                'high': high,
                'low': low,
                'close': close,
                'volume': volume
            })
            volumes.append(volume)
        
        # Criar DataFrame
        df = pd.DataFrame(prices, index=dates)
        
        print(f"✅ Dados gerados: {len(df)} registros")
        print(f"   Preço atual: ${df['close'].iloc[-1]:.2f}")
        print(f"   Volume atual: {df['volume'].iloc[-1]:,.0f}")
        
        # Testar indicadores técnicos
        print("\n🔍 Testando indicadores técnicos...")
        tech_indicators = TechnicalIndicators(verbose=True)
        indicators = tech_indicators.calculate_all_indicators(df)
        
        print(f"✅ Indicadores calculados: {len(indicators)} indicadores")
        
        # Verificar novos indicadores
        print("\n📊 Verificando novos indicadores:")
        
        # Volume Trend
        volume_trend_direction = indicators.get('volume_trend_direction', 0)
        volume_strength = indicators.get('volume_strength', 1)
        volume_momentum = indicators.get('volume_momentum', 0)
        
        print(f"   📈 Tendência de Volume: {volume_trend_direction}")
        print(f"   💪 Força do Volume: {volume_strength:.2f}")
        print(f"   🚀 Momentum do Volume: {volume_momentum:.2f}%")
        
        # Fibonacci
        retracement_pct = indicators.get('retracement_pct', 0)
        nearest_level = indicators.get('nearest_level', '')
        fib_levels = indicators.get('fib_levels', {})
        
        print(f"   📐 Retração Fibonacci: {retracement_pct:.1f}%")
        print(f"   🎯 Nível Mais Próximo: {nearest_level}")
        
        if fib_levels:
            print("   📊 Níveis Fibonacci:")
            for level_name, level_value in fib_levels.items():
                print(f"      {level_name}: ${level_value:.2f}")
        
        # Testar análise de sinal
        print("\n🎯 Testando análise de sinal...")
        from signal_generator import SignalGenerator
        
        signal_gen = SignalGenerator(verbose=True)
        
        # Simular análise de timeframe
        timeframe_analysis = signal_gen._analyze_timeframe(indicators, df['close'].iloc[-1])
        
        print(f"   📊 Direção: {timeframe_analysis.get('direction', 'NEUTRAL')}")
        print(f"   🎯 Confiança: {timeframe_analysis.get('confidence', 0)}")
        print(f"   📈 Sinais: {timeframe_analysis.get('signals', [])}")
        
        print("\n✅ Teste dos novos indicadores concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_new_indicators()
    if success:
        print("\n🎉 Novos indicadores funcionando corretamente!")
    else:
        print("\n💥 Problema encontrado nos novos indicadores!") 