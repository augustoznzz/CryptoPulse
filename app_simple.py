#!/usr/bin/env python3
"""
Versão Simplificada da Interface Web para Teste Rápido
"""

from flask import Flask, render_template, jsonify, request
import time
import threading

app = Flask(__name__)

@app.route('/')
def index():
    """Página principal da interface"""
    return render_template('index.html')

@app.route('/api/search-trades', methods=['POST'])
def search_trades():
    print("🔍 [API] Iniciando busca de oportunidades...")
    try:
        # Simular análise rápida para teste
        print("🔍 Simulando análise...")
        time.sleep(2)  # Simular tempo de processamento
        
        # Dados de exemplo (excluindo stablecoins)
        mock_results = [
            {
                'symbol': 'BTC',
                'signal': 'BTC/USDT 🔼 LONG\n📍 Entry: 65432.50\n🎯 Take-Profit Targets:\n✅ TP1: 67033.95\n✅ TP2: 68971.11\n✅ TP3: 72105.05\n✅ TP4: 77176.15\n❌ Stop-loss: 62055.68\n❌ Safe Stop-loss: 58828.91\n📈 Leverage: 2x',
                'type': 'LONG',
                'potential_gain': 2.45,
                'entry_price': 65432.50,
                'coin_name': 'Bitcoin',
                'momentum_score': 65.2,
                'market_cap_rank': 1
            },
            {
                'symbol': 'ETH',
                'signal': 'ETH/USDT 🔼 LONG\n📍 Entry: 3594.10\n🎯 Take-Profit Targets:\n✅ TP1: 3724.44\n✅ TP2: 3805.01\n✅ TP3: 3935.35\n✅ TP4: 4146.26\n❌ Stop-loss: 3489.50\n❌ Safe Stop-loss: 3383.19\n📈 Leverage: 2x',
                'type': 'LONG',
                'potential_gain': 3.62,
                'entry_price': 3594.10,
                'coin_name': 'Ethereum',
                'momentum_score': 62.8,
                'market_cap_rank': 2
            },
            {
                'symbol': 'SOL',
                'signal': 'SOL/USDT 🔼 LONG\n📍 Entry: 163.895\n🎯 Take-Profit Targets:\n✅ TP1: 170.784\n✅ TP2: 175.042\n✅ TP3: 181.931\n✅ TP4: 193.078\n❌ Stop-loss: 158.871\n❌ Safe Stop-loss: 152.748\n📈 Leverage: 2x',
                'type': 'LONG',
                'potential_gain': 4.20,
                'entry_price': 163.895,
                'coin_name': 'Solana',
                'momentum_score': 58.9,
                'market_cap_rank': 6
            }
        ]
        
        print("✅ Análise simulada concluída")
        
        return jsonify({
            'success': True,
            'results': mock_results,
            'total_analyzed': 10,
            'total_opportunities': 3,
            'analysis_time': 2.5,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
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
    print("🚀 Iniciando servidor CryptoPulse (versão de teste)...")
    print("📊 Simulando análise de criptomoedas")
    print("🌐 Acesse: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True) 