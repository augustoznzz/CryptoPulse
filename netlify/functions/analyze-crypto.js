const https = require('https');

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
    console.log('Iniciando análise de criptomoedas...');
    
    let targetCoins;
    let source = 'API';
    
    try {
      // Tentar obter dados da API
      targetCoins = await getTargetCryptocurrencies();
      console.log(`Criptomoedas obtidas da API: ${targetCoins.length}`);
    } catch (apiError) {
      console.log('API falhou, usando dados de fallback:', apiError.message);
      // Usar dados de fallback se a API falhar
      targetCoins = getFallbackData();
      source = 'Fallback';
    }
    
    if (targetCoins.length === 0) {
      throw new Error('Nenhuma criptomoeda disponível para análise');
    }
    
    // Gerar análise simples e rápida
    const analysisResults = generateSimpleAnalysis(targetCoins);
    console.log(`Análises geradas: ${analysisResults.length}`);
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        results: analysisResults,
        total_analyzed: targetCoins.length,
        timestamp: new Date().toISOString(),
        message: `Análise técnica das criptomoedas selecionadas concluída (${source})`,
        data_source: source
      })
    };
  } catch (error) {
    console.error('Erro na análise:', error.message);
    
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

// Dados de fallback para quando a API falhar
function getFallbackData() {
  const fallbackCoins = [
    {
      id: 'bitcoin',
      symbol: 'BTC',
      name: 'Bitcoin',
      current_price: 45000 + Math.random() * 5000,
      market_cap: 800000000000 + Math.random() * 100000000000,
      price_change_24h: (Math.random() - 0.5) * 10,
      price_change_percentage_24h: (Math.random() - 0.5) * 10,
      volume_24h: 20000000000 + Math.random() * 10000000000
    },
    {
      id: 'ethereum',
      symbol: 'ETH',
      name: 'Ethereum',
      current_price: 2800 + Math.random() * 300,
      market_cap: 300000000000 + Math.random() * 50000000000,
      price_change_24h: (Math.random() - 0.5) * 8,
      price_change_percentage_24h: (Math.random() - 0.5) * 8,
      volume_24h: 15000000000 + Math.random() * 8000000000
    },
    {
      id: 'ripple',
      symbol: 'XRP',
      name: 'XRP',
      current_price: 0.6 + Math.random() * 0.2,
      market_cap: 30000000000 + Math.random() * 10000000000,
      price_change_24h: (Math.random() - 0.5) * 6,
      price_change_percentage_24h: (Math.random() - 0.5) * 6,
      volume_24h: 2000000000 + Math.random() * 1000000000
    },
    {
      id: 'binancecoin',
      symbol: 'BNB',
      name: 'BNB',
      current_price: 320 + Math.random() * 40,
      market_cap: 50000000000 + Math.random() * 10000000000,
      price_change_24h: (Math.random() - 0.5) * 7,
      price_change_percentage_24h: (Math.random() - 0.5) * 7,
      volume_24h: 3000000000 + Math.random() * 2000000000
    },
    {
      id: 'solana',
      symbol: 'SOL',
      name: 'Solana',
      current_price: 100 + Math.random() * 20,
      market_cap: 40000000000 + Math.random() * 10000000000,
      price_change_24h: (Math.random() - 0.5) * 9,
      price_change_percentage_24h: (Math.random() - 0.5) * 9,
      volume_24h: 2500000000 + Math.random() * 1500000000
    }
  ];
  
  console.log(`Dados de fallback gerados: ${fallbackCoins.length} criptomoedas`);
  return fallbackCoins;
}

// Obter dados das criptomoedas específicas
function getTargetCryptocurrencies() {
  return new Promise((resolve, reject) => {
    // Buscar diretamente as criptomoedas específicas
    const coinIds = TARGET_CRYPTOCURRENCIES.join(',');
    const url = `https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=${coinIds}&order=market_cap_desc&sparkline=false&price_change_percentage=24h`;
    
    console.log('Fazendo requisição para CoinGecko API...');
    
    const req = https.get(url, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          console.log(`Resposta da API: ${res.statusCode} ${res.statusMessage}`);
          
          if (res.statusCode !== 200) {
            reject(new Error(`HTTP ${res.statusCode}: ${res.statusMessage}`));
            return;
          }
          
          const jsonData = JSON.parse(data);
          console.log(`Dados recebidos: ${jsonData.length} criptomoedas`);

          if (jsonData.length === 0) {
            reject(new Error('Nenhuma criptomoeda encontrada na API'));
            return;
          }

          const result = jsonData.map(coin => ({
            id: coin.id,
            symbol: coin.symbol.toUpperCase(),
            name: coin.name,
            current_price: coin.current_price,
            market_cap: coin.market_cap,
            price_change_24h: coin.price_change_24h,
            price_change_percentage_24h: coin.price_change_percentage_24h,
            volume_24h: coin.total_volume
          }));
          
          console.log(`Criptomoedas processadas: ${result.length}`);
          resolve(result);
        } catch (parseError) {
          console.error('Erro ao fazer parse dos dados:', parseError.message);
          reject(new Error('Erro ao processar dados da API'));
        }
      });
    });
    
    req.on('error', (err) => {
      console.error('Erro na requisição HTTPS:', err.message);
      reject(new Error('Erro de conexão com a API'));
    });
    
    // Timeout de 10 segundos
    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error('Timeout na requisição à API'));
    });
  });
}

// Gerar análise simples e rápida
function generateSimpleAnalysis(coins) {
  const results = [];
  
  for (const coin of coins) {
    try {
      // Análise básica baseada nos dados disponíveis
      const analysis = analyzeCoin(coin);
      
      if (analysis.score > 0.2) { // Score baixo para incluir mais resultados
        results.push({
          symbol: coin.symbol,
          name: coin.name,
          current_price: coin.current_price,
          price_change_24h: coin.price_change_percentage_24h,
          type: analysis.type,
          potential_gain: analysis.potentialGain,
          signal: analysis.description,
          score: analysis.score,
          volume_24h: coin.volume_24h
        });
      }
    } catch (error) {
      console.error(`Erro ao analisar ${coin.symbol}:`, error.message);
      continue;
    }
  }
  
  // Ordenar por score e retornar top 10
  return results
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);
}

// Analisar uma criptomoeda individual
function analyzeCoin(coin) {
  let score = 0.5; // Score base
  let type = 'NEUTRAL';
  let potentialGain = 10;
  
  // Análise baseada na variação de preço
  if (coin.price_change_percentage_24h > 3) {
    score += 0.2; // Tendência de alta
    type = 'LONG';
  } else if (coin.price_change_percentage_24h < -3) {
    score += 0.15; // Oportunidade de compra em baixa
    type = 'LONG';
  }
  
  // Análise baseada no volume
  if (coin.volume_24h > 1000000000) { // > 1B
    score += 0.2; // Volume muito alto
  } else if (coin.volume_24h > 100000000) { // > 100M
    score += 0.15; // Volume alto
  } else if (coin.volume_24h > 10000000) { // > 10M
    score += 0.1; // Volume médio
  }
  
  // Análise baseada no market cap
  if (coin.market_cap > 10000000000) { // > 10B
    score += 0.1; // Moeda estabelecida
  }
  
  // Normalizar score
  score = Math.max(0, Math.min(1, score));
  
  // Calcular potencial de ganho
  potentialGain = Math.round((score * 20 + 5) * 10) / 10; // 5% a 25%
  
  // Gerar descrição
  const description = generateDescription(coin, score);
  
  return {
    type,
    score,
    potentialGain,
    description
  };
}

// Gerar descrição da análise
function generateDescription(coin, score) {
  let description = `Análise Técnica ${coin.symbol}:\n`;
  
  // Tendência baseada na variação 24h
  if (coin.price_change_percentage_24h > 0) {
    description += `• Tendência: Bullish (+${coin.price_change_percentage_24h.toFixed(2)}% 24h)\n`;
  } else {
    description += `• Tendência: Bearish (${coin.price_change_percentage_24h.toFixed(2)}% 24h)\n`;
  }
  
  // Preço atual
  description += `• Preço atual: $${coin.current_price.toFixed(4)}\n`;
  
  // Volume
  if (coin.volume_24h > 1000000000) {
    description += `• Volume: Muito Alto ($${(coin.volume_24h / 1000000000).toFixed(2)}B)\n`;
  } else if (coin.volume_24h > 100000000) {
    description += `• Volume: Alto ($${(coin.volume_24h / 1000000).toFixed(2)}M)\n`;
  } else {
    description += `• Volume: Médio ($${(coin.volume_24h / 1000000).toFixed(2)}M)\n`;
  }
  
  // Market cap
  if (coin.market_cap > 10000000000) {
    description += `• Market Cap: Alto (estabelecido)\n`;
  } else {
    description += `• Market Cap: Médio (crescimento)\n`;
  }
  
  description += `\nEstratégia: ${score > 0.6 ? 'Compra' : 'Venda'} com alvo +${Math.round(score * 20 + 5)}%`;
  description += `\nConfiança: ${Math.round(score * 100)}%`;
  
  return description;
}
