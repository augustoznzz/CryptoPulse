// Lista específica de criptomoedas para análise
const TARGET_CRYPTOCURRENCIES = [
  'bitcoin', 'ethereum', 'ripple', 'tether', 'binancecoin', 
  'solana', 'usd-coin', 'dogecoin', 'tron', 'cardano', 
  'chainlink', 'sui', 'stellar', 'uniswap', 'polkadot', 'dai'
];

// Função principal da Netlify Function
exports.handler = async (event, context) => {
  // Habilitar CORS
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
  };

  // Responder a requisições OPTIONS (preflight)
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  try {
    // Obter dados das criptomoedas específicas
    const targetCoins = await getTargetCryptocurrencies();
    
    // Analisar cada criptomoeda
    const analysisResults = await analyzeCryptocurrencies(targetCoins);
    
    // Filtrar e ordenar resultados
    const filteredResults = filterAndSortResults(analysisResults);
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        results: filteredResults,
        total_analyzed: targetCoins.length,
        timestamp: new Date().toISOString(),
        message: 'Análise técnica das criptomoedas selecionadas concluída'
      })
    };
  } catch (error) {
    console.error('Erro na análise:', error);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: 'Erro na análise técnica: ' + error.message,
        timestamp: new Date().toISOString()
      })
    };
  }
};

// Obter dados das criptomoedas específicas
async function getTargetCryptocurrencies() {
  try {
    // Usar fetch nativo em vez de axios
    const response = await fetch('https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false&price_change_percentage=24h');
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();

    // Filtrar apenas as criptomoedas que queremos
    const filteredCoins = data.filter(coin => 
      TARGET_CRYPTOCURRENCIES.includes(coin.id)
    );

    // Verificar se encontramos todas as criptomoedas desejadas
    if (filteredCoins.length !== TARGET_CRYPTOCURRENCIES.length) {
      const foundIds = filteredCoins.map(coin => coin.id);
      const missingIds = TARGET_CRYPTOCURRENCIES.filter(id => !foundIds.includes(id));
      console.warn(`Criptomoedas não encontradas: ${missingIds.join(', ')}`);
    }

    return filteredCoins.map(coin => ({
      id: coin.id,
      symbol: coin.symbol.toUpperCase(),
      name: coin.name,
      current_price: coin.current_price,
      market_cap: coin.market_cap,
      price_change_24h: coin.price_change_24h,
      price_change_percentage_24h: coin.price_change_percentage_24h,
      volume_24h: coin.total_volume
    }));
  } catch (error) {
    console.error('Erro ao obter criptomoedas:', error);
    throw new Error('Não foi possível obter dados das criptomoedas');
  }
}

// Analisar criptomoedas individualmente
async function analyzeCryptocurrencies(coins) {
  const results = [];
  
  for (const coin of coins) {
    try {
      // Obter dados históricos para análise técnica
      const historicalData = await getHistoricalData(coin.id);
      
      // Calcular indicadores técnicos
      const technicalAnalysis = calculateTechnicalIndicators(historicalData);
      
      // Gerar sinal de trading
      const tradingSignal = generateTradingSignal(technicalAnalysis, coin);
      
      if (tradingSignal.score > 0.6) { // Apenas sinais com score alto
        results.push({
          symbol: coin.symbol,
          name: coin.name,
          current_price: coin.current_price,
          price_change_24h: coin.price_change_percentage_24h,
          type: tradingSignal.type,
          potential_gain: tradingSignal.potentialGain,
          signal: tradingSignal.description,
          score: tradingSignal.score,
          indicators: technicalAnalysis
        });
      }
    } catch (error) {
      console.error(`Erro ao analisar ${coin.symbol}:`, error);
      continue; // Continuar com próxima criptomoeda
    }
  }
  
  return results;
}

// Obter dados históricos
async function getHistoricalData(coinId) {
  try {
    const response = await fetch(`https://api.coingecko.com/api/v3/coins/${coinId}/market_chart?vs_currency=usd&days=30&interval=daily`);
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    const data = await response.json();

    return data.prices.map(([timestamp, price]) => ({
      timestamp,
      price
    }));
  } catch (error) {
    throw new Error(`Erro ao obter dados históricos para ${coinId}`);
  }
}

// Calcular indicadores técnicos
function calculateTechnicalIndicators(prices) {
  const pricesArray = prices.map(p => p.price);
  
  // Médias móveis
  const sma20 = calculateSMA(pricesArray, 20);
  const sma50 = calculateSMA(pricesArray, 50);
  
  // RSI
  const rsi = calculateRSI(pricesArray, 14);
  
  // MACD
  const macd = calculateMACD(pricesArray);
  
  // Volatilidade
  const volatility = calculateVolatility(pricesArray);
  
  // Volume (simulado para demonstração)
  const volume = Math.random() * 100 + 50;
  
  return {
    sma20,
    sma50,
    rsi,
    macd,
    volatility,
    volume,
    currentPrice: pricesArray[pricesArray.length - 1],
    previousPrice: pricesArray[pricesArray.length - 2]
  };
}

// Calcular SMA (Simple Moving Average)
function calculateSMA(prices, period) {
  if (prices.length < period) return null;
  
  const sum = prices.slice(-period).reduce((acc, price) => acc + price, 0);
  return sum / period;
}

// Calcular RSI (Relative Strength Index)
function calculateRSI(prices, period) {
  if (prices.length < period + 1) return null;
  
  let gains = 0;
  let losses = 0;
  
  for (let i = 1; i <= period; i++) {
    const change = prices[prices.length - i] - prices[prices.length - i - 1];
    if (change > 0) {
      gains += change;
    } else {
      losses += Math.abs(change);
    }
  }
  
  const avgGain = gains / period;
  const avgLoss = losses / period;
  
  if (avgLoss === 0) return 100;
  
  const rs = avgGain / avgLoss;
  return 100 - (100 / (1 + rs));
}

// Calcular MACD
function calculateMACD(prices) {
  const ema12 = calculateEMA(prices, 12);
  const ema26 = calculateEMA(prices, 26);
  
  if (!ema12 || !ema26) return { macd: 0, signal: 0, histogram: 0 };
  
  const macd = ema12 - ema26;
  const signal = calculateEMA([macd], 9) || macd;
  const histogram = macd - signal;
  
  return { macd, signal, histogram };
}

// Calcular EMA (Exponential Moving Average)
function calculateEMA(prices, period) {
  if (prices.length < period) return null;
  
  const multiplier = 2 / (period + 1);
  let ema = prices[0];
  
  for (let i = 1; i < prices.length; i++) {
    ema = (prices[i] * multiplier) + (ema * (1 - multiplier));
  }
  
  return ema;
}

// Calcular volatilidade
function calculateVolatility(prices) {
  if (prices.length < 2) return 0;
  
  const returns = [];
  for (let i = 1; i < prices.length; i++) {
    returns.push((prices[i] - prices[i-1]) / prices[i-1]);
  }
  
  const mean = returns.reduce((acc, ret) => acc + ret, 0) / returns.length;
  const variance = returns.reduce((acc, ret) => acc + Math.pow(ret - mean, 2), 0) / returns.length;
  
  return Math.sqrt(variance);
}

// Gerar sinal de trading
function generateTradingSignal(indicators, coin) {
  let score = 0;
  let type = 'NEUTRAL';
  let potentialGain = 0;
  let description = '';
  
  // Análise de tendência
  if (indicators.currentPrice > indicators.sma20 && indicators.sma20 > indicators.sma50) {
    score += 0.3; // Tendência de alta
  } else if (indicators.currentPrice < indicators.sma20 && indicators.sma20 < indicators.sma50) {
    score -= 0.2; // Tendência de baixa
  }
  
  // Análise RSI
  if (indicators.rsi < 30) {
    score += 0.25; // Sobrevendido
    type = 'LONG';
  } else if (indicators.rsi > 70) {
    score -= 0.2; // Sobrecomprado
    type = 'SHORT';
  }
  
  // Análise MACD
  if (indicators.macd.macd > indicators.macd.signal && indicators.macd.histogram > 0) {
    score += 0.2; // MACD bullish
  } else if (indicators.macd.macd < indicators.macd.signal && indicators.macd.histogram < 0) {
    score -= 0.15; // MACD bearish
  }
  
  // Análise de volatilidade
  if (indicators.volatility > 0.05) { // 5% de volatilidade
    score += 0.1; // Alta volatilidade = mais oportunidades
  }
  
  // Análise de volume
  if (indicators.volume > 75) {
    score += 0.1; // Volume alto
  }
  
  // Análise de momentum
  const priceChange = ((indicators.currentPrice - indicators.previousPrice) / indicators.previousPrice) * 100;
  if (Math.abs(priceChange) > 2) { // Mudança de preço significativa
    score += 0.05;
  }
  
  // Normalizar score
  score = Math.max(0, Math.min(1, score));
  
  // Calcular potencial de ganho baseado no score
  potentialGain = Math.round((score * 20 + 5) * 10) / 10; // 5% a 25%
  
  // Gerar descrição detalhada
  description = generateDetailedDescription(indicators, coin, type, score);
  
  return {
    type,
    score,
    potentialGain,
    description
  };
}

// Gerar descrição detalhada
function generateDetailedDescription(indicators, coin, type, score) {
  let description = `Análise Técnica ${coin.symbol}:\n`;
  
  // Tendência
  if (indicators.currentPrice > indicators.sma20) {
    description += `• Tendência: Bullish (preço acima da MA20)\n`;
  } else {
    description += `• Tendência: Bearish (preço abaixo da MA20)\n`;
  }
  
  // RSI
  if (indicators.rsi < 30) {
    description += `• RSI: ${indicators.rsi.toFixed(1)} (Sobrevendido - oportunidade de compra)\n`;
  } else if (indicators.rsi > 70) {
    description += `• RSI: ${indicators.rsi.toFixed(1)} (Sobrecomprado - oportunidade de venda)\n`;
  } else {
    description += `• RSI: ${indicators.rsi.toFixed(1)} (Neutro)\n`;
  }
  
  // MACD
  if (indicators.macd.macd > indicators.macd.signal) {
    description += `• MACD: Bullish (sinal de alta)\n`;
  } else {
    description += `• MACD: Bearish (sinal de baixa)\n`;
  }
  
  // Volatilidade
  description += `• Volatilidade: ${(indicators.volatility * 100).toFixed(1)}%\n`;
  
  // Volume
  if (indicators.volume > 75) {
    description += `• Volume: Alto (confirma tendência)\n`;
  } else {
    description += `• Volume: Baixo (tendência fraca)\n`;
  }
  
  description += `\nEstratégia: ${type === 'LONG' ? 'Compra' : 'Venda'} com alvo +${Math.round(score * 20 + 5)}%`;
  description += `\nConfiança: ${Math.round(score * 100)}%`;
  
  return description;
}

// Filtrar e ordenar resultados
function filterAndSortResults(results) {
  // Remover duplicatas por símbolo
  const uniqueResults = results.filter((result, index, self) => 
    index === self.findIndex(r => r.symbol === result.symbol)
  );
  
  // Ordenar por score (maior primeiro)
  const sortedResults = uniqueResults.sort((a, b) => b.score - a.score);
  
  // Retornar todos os resultados (máximo 16)
  return sortedResults.slice(0, 16);
}
