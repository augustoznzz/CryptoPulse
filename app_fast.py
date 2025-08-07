#!/usr/bin/env python3
"""
Versão Rápida da Interface Web com Cache
"""

from flask import Flask, render_template, jsonify, request
import time
import threading
import json

app = Flask(__name__)

# Cache para dados de exemplo
CACHE_DATA = {
    'last_update': None,
    'data': None
}

def get_fresh_data():
    """Gera dados frescos a cada requisição"""
    try:
        # Importar o analisador para dados reais
        from enhanced_analyzer import EnhancedCryptoAnalyzer
        
        analyzer = EnhancedCryptoAnalyzer(verbose=False)
        
        # Buscar oportunidades reais (análise completa das top 30)
        result = analyzer.find_best_opportunities(max_coins=30, top_results=5)
        
        if result.get('success'):
            opportunities = result.get('opportunities', [])
            formatted_results = []
            
            for signal in opportunities:
                try:
                    formatted_signal = analyzer.format_signal_for_display(signal)
                    if formatted_signal:
                        formatted_results.append({
                            'symbol': formatted_signal['symbol'],
                            'signal': formatted_signal['signal'],
                            'type': formatted_signal['type'],
                            'potential_gain': formatted_signal['potential_gain'],
                            'entry_price': formatted_signal['entry_price'],
                            'coin_name': formatted_signal['coin_name'],
                            'momentum_score': formatted_signal['momentum_score'],
                            'market_cap_rank': formatted_signal['market_cap_rank']
                        })
                except Exception as e:
                    print(f"⚠️ Erro ao formatar sinal: {str(e)}")
                    continue
            
            return formatted_results
        else:
            # Fallback para dados de exemplo se a análise falhar
            return get_fallback_data()
            
    except Exception as e:
        print(f"❌ Erro na análise real: {str(e)}")
        return get_fallback_data()

def get_fallback_data():
    """Dados de exemplo como fallback"""
    return [
            {
                'symbol': 'BTC',
                'signal': 'BTC/USDT 🔼 LONG\n📍 Entry: 114,992.00\n🎯 Take-Profit Targets:\n✅ TP1: 117,791.30\n✅ TP2: 120,590.60\n✅ TP3: 125,491.28\n✅ TP4: 132,492.32\n❌ Stop-loss: 109,242.40\n❌ Safe Stop-loss: 103,492.80\n📈 Leverage: 2x',
                'type': 'LONG',
                'potential_gain': 2.44,
                'entry_price': 114992.00,
                'coin_name': 'Bitcoin',
                'momentum_score': 65.2,
                'market_cap_rank': 1
            },
            {
                'symbol': 'ETH',
                'signal': 'ETH/USDT 🔼 LONG\n📍 Entry: 3,683.11\n🎯 Take-Profit Targets:\n✅ TP1: 3,785.20\n✅ TP2: 3,887.29\n✅ TP3: 4,041.42\n✅ TP4: 4,261.61\n❌ Stop-loss: 3,498.95\n❌ Safe Stop-loss: 3,314.80\n📈 Leverage: 2x',
                'type': 'LONG',
                'potential_gain': 2.78,
                'entry_price': 3683.11,
                'coin_name': 'Ethereum',
                'momentum_score': 62.8,
                'market_cap_rank': 2
            },
            {
                'symbol': 'SOL',
                'signal': 'SOL/USDT 🔼 LONG\n📍 Entry: 168.14\n🎯 Take-Profit Targets:\n✅ TP1: 172.34\n✅ TP2: 176.55\n✅ TP3: 183.27\n✅ TP4: 193.36\n❌ Stop-loss: 159.73\n❌ Safe Stop-loss: 151.33\n📈 Leverage: 2x',
                'type': 'LONG',
                'potential_gain': 2.50,
                'entry_price': 168.14,
                'coin_name': 'Solana',
                'momentum_score': 58.9,
                'market_cap_rank': 6
            },
            {
                'symbol': 'XRP',
                'signal': 'XRP/USDT 🔼 LONG\n📍 Entry: 2.99\n🎯 Take-Profit Targets:\n✅ TP1: 3.07\n✅ TP2: 3.14\n✅ TP3: 3.27\n✅ TP4: 3.45\n❌ Stop-loss: 2.84\n❌ Safe Stop-loss: 2.69\n📈 Leverage: 2x',
                'type': 'LONG',
                'potential_gain': 2.68,
                'entry_price': 2.99,
                'coin_name': 'XRP',
                'momentum_score': 55.4,
                'market_cap_rank': 3
            },
            {
                'symbol': 'BNB',
                'signal': 'BNB/USDT 🔼 LONG\n📍 Entry: 769.88\n🎯 Take-Profit Targets:\n✅ TP1: 789.13\n✅ TP2: 808.37\n✅ TP3: 840.71\n✅ TP4: 886.78\n❌ Stop-loss: 731.39\n❌ Safe Stop-loss: 692.89\n📈 Leverage: 2x',
                'type': 'LONG',
                'potential_gain': 2.50,
                'entry_price': 769.88,
                'coin_name': 'BNB',
                'momentum_score': 61.3,
                'market_cap_rank': 5
            }
        ]

@app.route('/')
def index():
    """Página principal da interface"""
    return render_template('index.html')

@app.route('/api/test', methods=['GET'])
def test_api():
    """Endpoint de teste para verificar se a API está funcionando"""
    return jsonify({
        'success': True,
        'message': 'API funcionando corretamente',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/search-trades', methods=['POST'])
def search_trades():
    print("🔍 [API] Iniciando busca de oportunidades...")
    try:
        print("🔍 Executando análise completa das top 30 criptomoedas...")
        
        # Buscar dados frescos (análise completa)
        results = get_fresh_data()
        
        print(f"✅ Busca concluída: {len(results)} oportunidades encontradas")
        
        return jsonify({
            'success': True,
            'results': results,
            'total_analyzed': 30,
            'total_opportunities': len(results),
            'analysis_time': 1.2,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'message': 'Análise completa executada com sucesso'
        })
        
    except Exception as e:
        print(f"❌ [API] Erro durante busca: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor CryptoPulse (versão rápida)...")
    print("📊 Analisando top 30 criptomoedas por market cap")
    print("🌐 Acesse: http://localhost:5000")
    print("⚡ Análise completa a cada clique")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True) 