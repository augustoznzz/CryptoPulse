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
    console.log('Starting cryptocurrency analysis...');
    
    let targetCoins;
    let source = 'API';
    
    try {
      // Tentar obter dados da API
      targetCoins = await getTargetCryptocurrencies();
      console.log(`Cryptocurrencies obtained from API: ${targetCoins.length}`);
    } catch (apiError) {
      console.log('API failed, using fallback data:', apiError.message);
      // Usar dados de fallback se a API falhar
      targetCoins = getFallbackData();
      source = 'Fallback';
    }
    
    if (targetCoins.length === 0) {
      throw new Error('No cryptocurrencies available for analysis');
    }
    
    // Generate simple and fast analysis
    const analysisResults = generateSimpleAnalysis(targetCoins);
    console.log(`Analyses generated: ${analysisResults.length}`);
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        results: analysisResults,
        total_analyzed: targetCoins.length,
        timestamp: new Date().toISOString().split('T')[0],
        message: `Technical analysis of selected cryptocurrencies completed (${source})`,
        data_source: source
      })
    };
  } catch (error) {
    console.error('Analysis error:', error.message);
    
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: 'Technical analysis error: ' + error.message,
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
      current_price: 85000 + Math.random() * 20000, // $85k - $105k
      market_cap: 1600000000000 + Math.random() * 200000000000, // $1.6T - $1.8T
      price_change_24h: (Math.random() - 0.5) * 8000, // ±$4k variation
      price_change_percentage_24h: (Math.random() - 0.5) * 8, // ±4% variation
      volume_24h: 30000000000 + Math.random() * 20000000000 // $30B - $50B
    },
    {
      id: 'ethereum',
      symbol: 'ETH',
      name: 'Ethereum',
      current_price: 4500 + Math.random() * 1000, // $4.5k - $5.5k
      market_cap: 500000000000 + Math.random() * 100000000000, // $500B - $600B
      price_change_24h: (Math.random() - 0.5) * 400, // ±$200 variation
      price_change_percentage_24h: (Math.random() - 0.5) * 6, // ±3% variation
      volume_24h: 20000000000 + Math.random() * 10000000000 // $20B - $30B
    },
    {
      id: 'ripple',
      symbol: 'XRP',
      name: 'XRP',
      current_price: 0.8 + Math.random() * 0.4, // $0.8 - $1.2
      market_cap: 40000000000 + Math.random() * 20000000000, // $40B - $60B
      price_change_24h: (Math.random() - 0.5) * 0.2, // ±$0.1 variation
      price_change_percentage_24h: (Math.random() - 0.5) * 5, // ±2.5% variation
      volume_24h: 3000000000 + Math.random() * 2000000000 // $3B - $5B
    },
    {
      id: 'binancecoin',
      symbol: 'BNB',
      name: 'BNB',
      current_price: 600 + Math.random() * 100, // $600 - $700
      market_cap: 90000000000 + Math.random() * 20000000000, // $90B - $110B
      price_change_24h: (Math.random() - 0.5) * 60, // ±$30 variation
      price_change_percentage_24h: (Math.random() - 0.5) * 4, // ±2% variation
      volume_24h: 5000000000 + Math.random() * 3000000000 // $5B - $8B
    },
    {
      id: 'solana',
      symbol: 'SOL',
      name: 'Solana',
      current_price: 180 + Math.random() * 40, // $180 - $220
      market_cap: 70000000000 + Math.random() * 20000000000, // $70B - $90B
      price_change_24h: (Math.random() - 0.5) * 20, // ±$10 variation
      price_change_percentage_24h: (Math.random() - 0.5) * 7, // ±3.5% variation
      volume_24h: 4000000000 + Math.random() * 2000000000 // $4B - $6B
    }
  ];
  
  console.log(`Fallback data generated: ${fallbackCoins.length} cryptocurrencies`);
  return fallbackCoins;
}

// Obter dados das criptomoedas específicas
function getTargetCryptocurrencies() {
  return new Promise((resolve, reject) => {
    // Buscar diretamente as criptomoedas específicas
    const coinIds = TARGET_CRYPTOCURRENCIES.join(',');
    const url = `https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=${coinIds}&order=market_cap_desc&sparkline=false&price_change_percentage=24h`;
    
    console.log('Making request to CoinGecko API...');
    
    const req = https.get(url, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          console.log(`API Response: ${res.statusCode} ${res.statusMessage}`);
          
          if (res.statusCode !== 200) {
            reject(new Error(`HTTP ${res.statusCode}: ${res.statusMessage}`));
            return;
          }
          
          const jsonData = JSON.parse(data);
          console.log(`Data received: ${jsonData.length} cryptocurrencies`);

                      if (jsonData.length === 0) {
              reject(new Error('No cryptocurrencies found in API'));
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
          
          console.log(`Cryptocurrencies processed: ${result.length}`);
          resolve(result);
        } catch (parseError) {
          console.error('Error parsing data:', parseError.message);
          reject(new Error('Error processing API data'));
        }
      });
    });
    
    req.on('error', (err) => {
      console.error('HTTPS request error:', err.message);
      reject(new Error('API connection error'));
    });
    
    // Timeout de 10 segundos
    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error('API request timeout'));
    });
  });
}

// Gerar análise simples e rápida
function generateSimpleAnalysis(coins) {
  const results = [];
  
  for (const coin of coins) {
    try {
          // Basic analysis based on available data
    const analysis = analyzeCoin(coin);
      
              if (analysis.score > 0.2) { // Low score to include more results
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
        console.error(`Error analyzing ${coin.symbol}:`, error.message);
        continue;
      }
  }
  
      // Sort by score and return top 10
  return results
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);
}

// Analisar uma criptomoeda individual
function analyzeCoin(coin) {
  let score = 0.5; // Score base
  let type = 'NEUTRAL';
  let potentialGain = 10;
  
  // Analysis based on price variation
  if (coin.price_change_percentage_24h > 3) {
    score += 0.2; // Uptrend
    type = 'LONG';
  } else if (coin.price_change_percentage_24h < -3) {
    score += 0.15; // Opportunity to short at high
    type = 'SHORT';
  }
  
  // Analysis based on volume
  if (coin.volume_24h > 1000000000) { // > 1B
    score += 0.2; // Very high volume
  } else if (coin.volume_24h > 100000000) { // > 100M
    score += 0.15; // High volume
  } else if (coin.volume_24h > 10000000) { // > 10M
    score += 0.1; // Medium volume
  }
  
  // Analysis based on market cap
  if (coin.market_cap > 10000000000) { // > 10B
    score += 0.1; // Established coin
  }
  
  // Normalize score
  score = Math.max(0, Math.min(1, score));
  
  // Calculate potential gain
  potentialGain = Math.round((score * 20 + 5) * 10) / 10; // 5% to 25%
  
  // Determine type based on potential gain and score
  if (potentialGain > 15 && score > 0.6) {
    type = 'LONG'; // High potential = Buy
  } else if (potentialGain < 10 || score < 0.4) {
    type = 'SHORT'; // Low potential = Sell
  }
  
  // Generate description
  const description = generateDescription(coin, score);
  
  return {
    type,
    score,
    potentialGain,
    description
  };
}

// Generate analysis description
function generateDescription(coin, score) {
  let description = `Technical Analysis ${coin.symbol}:\n`;
  
  // Trend based on 24h variation
  if (coin.price_change_percentage_24h > 0) {
    description += `• Trend: Bullish (+${coin.price_change_percentage_24h.toFixed(2)}% 24h)\n`;
  } else {
    description += `• Trend: Bearish (${coin.price_change_percentage_24h.toFixed(2)}% 24h)\n`;
  }
  
  // Current price - format without decimals and with thousand separators
  const formattedPrice = Math.round(coin.current_price).toLocaleString('en-US');
  description += `• Current price: $${formattedPrice}\n`;
  
  // Volume - format with appropriate units and thousand separators
  if (coin.volume_24h > 1000000000) {
    const volumeB = (coin.volume_24h / 1000000000).toFixed(1);
    description += `• Volume: Very High ($${volumeB}B)\n`;
  } else if (coin.volume_24h > 100000000) {
    const volumeM = (coin.volume_24h / 1000000).toFixed(1);
    description += `• Volume: High ($${volumeM}M)\n`;
  } else {
    const volumeM = (coin.volume_24h / 1000000).toFixed(1);
    description += `• Volume: Medium ($${volumeM}M)\n`;
  }
  
  // Market cap - format with appropriate units
  if (coin.market_cap > 1000000000000) {
    const marketCapT = (coin.market_cap / 1000000000000).toFixed(1);
    description += `• Market Cap: High ($${marketCapT}T)\n`;
  } else if (coin.market_cap > 10000000000) {
    const marketCapB = (coin.market_cap / 1000000000).toFixed(1);
    description += `• Market Cap: High ($${marketCapB}B)\n`;
  } else {
    const marketCapB = (coin.market_cap / 1000000000).toFixed(1);
    description += `• Market Cap: Medium ($${marketCapB}B)\n`;
  }
  
  description += `\nStrategy: ${score > 0.6 ? 'Buy' : 'Sell'} with target +${Math.round(score * 20 + 5)}%`;
  description += `\nConfidence: ${Math.round(score * 100)}%`;
  
  return description;
}
