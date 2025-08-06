# Cryptocurrency Market Analysis Tool

Um software completo de análise técnica de criptomoedas que gera sinais de trading precisos com pontos de entrada, alvos de lucro e stop-losses baseados em análise multi-timeframe.

## 🚀 Características

- **Análise Multi-Timeframe**: Analisa dados de 1h, 4h e 1d para decisões mais precisas
- **Indicadores Técnicos Avançados**: SMA, EMA, RSI, MACD, Bandas de Bollinger
- **Matemática Avançada**: Regressão linear, análise de volatilidade, níveis de Fibonacci
- **Suporte a Múltiplas Exchanges**: Coinbase, Kraken, Binance, Bitfinex com fallback automático
- **Modo Demo**: Funciona mesmo quando exchanges não estão disponíveis
- **Sinais Precisos**: Gera recomendações LONG/SHORT com leverages calculadas

## 📦 Instalação

As dependências são instaladas automaticamente. O sistema requer:

```bash
pip install ccxt pandas numpy scipy scikit-learn
```

## 🛠 Como Usar

### Análise em Tempo Real
```bash
python main.py --moeda BTC
python main.py --moeda ETH
python main.py --moeda ADA
```

### Modo Demo (para testes)
```bash
python main.py --moeda BTC --demo
```

### Modo Verbose (com logs detalhados)
```bash
python main.py --moeda BTC --verbose
```

### Especificar Exchange
```bash
python main.py --moeda BTC --exchange coinbase
python main.py --moeda BTC --exchange kraken
```

## 📊 Formato de Saída

O software gera sinais no formato exato solicitado:

```
BTC/USDT 🔼 LONG
📍 Entry: 65432.50
🎯 Take-Profit Targets:
✅ TP1: 67033.95
✅ TP2: 68971.11
✅ TP3: 72105.05
✅ TP4: 77176.15
❌ Stop-loss: 62055.68
❌ Safe Stop-loss: 58828.91
📈 Leverage: 2x
```

## 🔧 Indicadores Implementados

### Médias Móveis
- **SMA 20/50**: Identificação de tendências
- **EMA 12/26**: Sinais de momentum

### Osciladores
- **RSI (14)**: Detecção de sobrecompra (>70) e sobrevenda (<30)
- **MACD**: Cruzamentos de sinal e análise de histograma

### Volatilidade
- **Bandas de Bollinger**: Medição de volatilidade e reversões
- **Desvio Padrão**: Cálculo de risco

### Análise Matemática
- **Regressão Linear**: Previsão de tendências futuras
- **Fibonacci**: Cálculo de alvos de lucro
- **Suporte/Resistência**: Identificação automática de níveis

## 🎯 Cálculo de Alvos

### Take-Profit (Fibonacci)
- **TP1**: 61.8% da extensão base
- **TP2**: 100% da extensão base  
- **TP3**: 161.8% da extensão base
- **TP4**: 261.8% da extensão base

### Stop-Loss
- **Stop-loss**: Baseado em suporte/resistência
- **Safe Stop-loss**: Mais conservador baseado em volatilidade

### Leverage
- **Volatilidade < 5%**: Leverage 5x
- **Volatilidade < 10%**: Leverage 3x
- **Volatilidade < 20%**: Leverage 2x
- **Volatilidade > 20%**: Leverage 1x

## 🔄 Sistema de Fallback

1. **Coinbase** (primário)
2. **Kraken** (fallback)
3. **Binance** (fallback)
4. **Bitfinex** (fallback)
5. **Modo Demo** (último recurso)

## 📋 Moedas Suportadas

- BTC/USDT
- ETH/USDT  
- ADA/USDT
- XRP/USDT
- DOT/USDT
- LINK/USDT
- SOL/USDT
- E qualquer par disponível nas exchanges

## 🧮 Algoritmo de Decisão

O sistema analisa múltiplos timeframes e usa:

1. **Concordância entre timeframes**: Mínimo 60% de acordo
2. **Peso dos indicadores**: RSI, MACD, médias móveis
3. **Confirmação de volume**: Volume acima da média
4. **Tendência matemática**: Regressão linear
5. **Posição de preço**: Relativa aos máximos/mínimos

## ⚡ Performance

- **Tempo de análise**: 2-5 segundos
- **Precisão de preços**: Até 8 casas decimais
- **Dados históricos**: 500 períodos por timeframe
- **Atualizações**: Tempo real via APIs

## 🛡 Tratamento de Erros

- **APIs indisponíveis**: Fallback automático
- **Dados insuficientes**: Mensagens claras
- **Símbolos inválidos**: Validação de entrada
- **Rate limiting**: Controle automático de frequência

## 📈 Exemplo de Uso

```bash
# Análise completa do Bitcoin
python main.py --moeda BTC --verbose

# Resultado:
# [DEBUG] Starting analysis for BTC/USDT
# [DATA] Successfully initialized Coinbase Advanced exchange
# [DEBUG] Fetching data for 1h timeframe
# [TECH] Calculated all technical indicators
# [SIGNAL] Generated LONG signal with 2x leverage
# 
# BTC/USDT 🔼 LONG
# 📍 Entry: 65432.50
# 🎯 Take-Profit Targets:
# ✅ TP1: 67033.95
# ✅ TP2: 68971.11  
# ✅ TP3: 72105.05
# ✅ TP4: 77176.15
# ❌ Stop-loss: 62055.68
# ❌ Safe Stop-loss: 58828.91
# 📈 Leverage: 2x
```

## 🔍 Arquitetura do Sistema

- **main.py**: Interface de linha de comando
- **crypto_analyzer.py**: Coordenador principal
- **data_fetcher.py**: Obtenção de dados das exchanges
- **technical_indicators.py**: Cálculo de indicadores
- **signal_generator.py**: Geração de sinais
- **utils.py**: Funções utilitárias

## ⚠ Aviso Legal

Este software é apenas para fins educacionais e de análise. Não constitui aconselhamento financeiro. Trading de criptomoedas envolve riscos significativos.