#!/usr/bin/env python3
"""
Web Interface for Cryptocurrency Analysis
Simple Flask web interface for crypto trading analysis
"""

from flask import Flask, render_template, jsonify, request
import threading
import time
from enhanced_analyzer import EnhancedCryptoAnalyzer

app = Flask(__name__)

# Ative o modo verbose ao instanciar o EnhancedCryptoAnalyzer
enhanced_analyzer = EnhancedCryptoAnalyzer(verbose=True)

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
    print("🔍 [API] Iniciando busca de oportunidades no mercado de criptomoedas...")
    try:
        print("🔍 Iniciando análise completa do mercado de criptomoedas...")
        
        # Use o analisador aprimorado para buscar oportunidades das top 30 criptomoedas por market cap
        # Análise completa a cada clique (sem cache)
        result = enhanced_analyzer.find_best_opportunities(max_coins=30, top_results=5)
        
        print("✅ [API] Busca finalizada.")
        
        if result.get('success'):
            opportunities = result.get('opportunities', [])
            formatted_results = []
            
            print(f"✅ Análise concluída: {len(opportunities)} oportunidades encontradas")
            
            for signal in opportunities:
                try:
                    formatted_signal = enhanced_analyzer.format_signal_for_display(signal)
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
                except Exception as format_error:
                    print(f"⚠️ Erro ao formatar sinal para {signal.get('symbol', 'Unknown')}: {str(format_error)}")
                    continue
            
            # Retorna as melhores oportunidades das top 50 criptomoedas (já ordenadas por score)
            top_results = formatted_results[:5]  # Top 5 oportunidades
            
            return jsonify({
                'success': True,
                'results': top_results,
                'total_analyzed': result.get('total_analyzed', 0),
                'total_opportunities': result.get('total_opportunities', 0),
                'analysis_time': result.get('analysis_time', 0),
                'timestamp': result.get('timestamp', time.strftime('%Y-%m-%d %H:%M:%S'))
            })
            
        else:
            error_msg = result.get('error', 'Erro desconhecido durante análise')
            print(f"❌ Erro na análise: {error_msg}")
            return jsonify({
                'success': False,
                'error': f'Erro na análise: {error_msg}'
            }), 500
            
    except Exception as e:
        print(f"❌ [API] Erro durante busca: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': f'Erro interno: {str(e)}'
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando servidor CryptoPulse...")
    print("📊 Analisando top 50 criptomoedas por market cap")
    print("🌐 Acesse: http://localhost:5000")
    print("⏱️  A primeira análise pode demorar alguns minutos...")
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)