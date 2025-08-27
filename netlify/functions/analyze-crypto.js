const https = require('https');

// Sistema de rate limiting baseado em IP
const rateLimitStore = new Map(); // IP -> { lastRequest: timestamp, count: number }

// Lista específica de criptomoedas para análise
const TARGET_CRYPTOCURRENCIES = [
  'bitcoin', 'ethereum', 'ripple', 'tether', 'binancecoin', 
  'solana', 'usd-coin', 'dogecoin', 'tron', 'cardano', 
  'chainlink', 'sui', 'stellar', 'uniswap', 'polkadot', 'dai'
];

// Função para obter IP real do usuário
function getClientIP(event) {
  // Netlify Functions pode ter diferentes headers para IP
  const headers = event.headers || {};
  
  // Tentar diferentes headers de IP
  const ip = headers['x-forwarded-for'] || 
             headers['x-real-ip'] || 
             headers['cf-connecting-ip'] || 
             headers['x-client-ip'] ||
             'unknown';
  
  // Se x-forwarded-for contém múltiplos IPs, pegar o primeiro
  return ip.split(',')[0].trim();
}

// Função para verificar rate limit
function checkRateLimit(ip) {
  const now = Date.now(); // Usar timestamp do servidor, não do cliente
  const oneHour = 60 * 60 * 1000; // 1 hora em milissegundos
  
  if (!rateLimitStore.has(ip)) {
    // Primeira solicitação deste IP
    rateLimitStore.set(ip, {
      lastRequest: now,
      count: 1
    });
    return { allowed: true, remainingTime: 0 };
  }
  
  const record = rateLimitStore.get(ip);
  const timeSinceLastRequest = now - record.lastRequest;
  
  if (timeSinceLastRequest < oneHour) {
    // Ainda dentro do período de 1 hora
    const remainingTime = Math.ceil((oneHour - timeSinceLastRequest) / 1000 / 60); // em minutos
    return { 
      allowed: false, 
      remainingTime,
      message: `Rate limit exceeded. Try again in ${remainingTime} minutes.`
    };
  } else {
    // Passou 1 hora, resetar contador
    rateLimitStore.set(ip, {
      lastRequest: now,
      count: 1
    });
    return { allowed: true, remainingTime: 0 };
  }
}

// Função para limpar IPs antigos (manutenção)
function cleanupOldIPs() {
  const now = Date.now();
  const oneDay = 24 * 60 * 60 * 1000; // 1 dia
  
  for (const [ip, record] of rateLimitStore.entries()) {
    if (now - record.lastRequest > oneDay) {
      rateLimitStore.delete(ip);
    }
  }
}

// Limpar IPs antigos a cada 100 solicitações
let requestCount = 0;

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
    // Obter IP do cliente
    const clientIP = getClientIP(event);
    console.log(`🔍 Request from IP: ${clientIP}`);
    
    // Verificar rate limit
    const rateLimitCheck = checkRateLimit(clientIP);
    
    if (!rateLimitCheck.allowed) {
      console.log(`🚫 Rate limit exceeded for IP ${clientIP}: ${rateLimitCheck.message}`);
      return {
        statusCode: 429, // Too Many Requests
        headers,
        body: JSON.stringify({
          success: false,
          error: 'Rate limit exceeded',
          message: rateLimitCheck.message,
          remainingTime: rateLimitCheck.remainingTime,
          timestamp: new Date().toISOString()
        })
      };
    }
    
    // Incrementar contador de solicitações para limpeza
    requestCount++;
    if (requestCount % 100 === 0) {
      cleanupOldIPs();
      console.log(`🧹 Cleaned up old IPs. Current store size: ${rateLimitStore.size}`);
    }
    
    console.log('✅ Rate limit check passed, starting cryptocurrency analysis...');
    
    let targetCoins;
    let source = 'API';
    let retryCount = 0;
    const maxRetries = 3;
    
    // Tentar obter dados da API com retry logic
    while (retryCount < maxRetries) {
      try {
        console.log(`Attempt ${retryCount + 1} to fetch data from CoinGecko API...`);
        targetCoins = await getTargetCryptocurrencies();
        
        if (targetCoins && targetCoins.length > 0) {
          console.log(`✅ Success! Cryptocurrencies obtained from API: ${targetCoins.length}`);
          console.log(`Sample real data - BTC price: $${targetCoins.find(c => c.symbol === 'BTC')?.current_price}`);
          source = 'Real-Time API';
          break; // Sucesso, sair do loop
        } else {
          throw new Error('API returned empty data');
        }
      } catch (apiError) {
        retryCount++;
        console.log(`❌ API attempt ${retryCount} failed:`, apiError.message);
        
        if (retryCount >= maxRetries) {
          console.log('🚨 All API attempts failed, using fallback data');
          targetCoins = getFallbackData();
          source = 'Fallback (API failed)';
        } else {
          console.log(`⏳ Waiting 2 seconds before retry ${retryCount + 1}...`);
          await new Promise(resolve => setTimeout(resolve, 2000)); // Esperar 2 segundos
        }
      }
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
        data_source: source,
        api_attempts: retryCount,
        rate_limit_info: {
          ip: clientIP,
          next_request_allowed: new Date(Date.now() + 60 * 60 * 1000).toISOString()
        }
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
      current_price: 95000 + Math.random() * 10000, // $95k - $105k (mais realista)
      market_cap: 1800000000000 + Math.random() * 200000000000, // $1.8T - $2.0T
      price_change_24h: (Math.random() - 0.5) * 6000, // ±$3k variation
      price_change_percentage_24h: (Math.random() - 0.5) * 6, // ±3% variation
      volume_24h: 35000000000 + Math.random() * 15000000000 // $35B - $50B
    },
    {
      id: 'ethereum',
      symbol: 'ETH',
      name: 'Ethereum',
      current_price: 5200 + Math.random() * 800, // $5.2k - $6.0k (mais realista)
      market_cap: 600000000000 + Math.random() * 100000000000, // $600B - $700B
      price_change_24h: (Math.random() - 0.5) * 300, // ±$150 variation
      price_change_percentage_24h: (Math.random() - 0.5) * 5, // ±2.5% variation
      volume_24h: 25000000000 + Math.random() * 10000000000 // $25B - $35B
    },
    {
      id: 'ripple',
      symbol: 'XRP',
      name: 'XRP',
      current_price: 0.95 + Math.random() * 0.3, // $0.95 - $1.25 (mais realista)
      market_cap: 50000000000 + Math.random() * 20000000000, // $50B - $70B
      price_change_24h: (Math.random() - 0.5) * 0.15, // ±$0.075 variation
      price_change_percentage_24h: (Math.random() - 0.5) * 4, // ±2% variation
      volume_24h: 4000000000 + Math.random() * 2000000000 // $4B - $6B
    },
    {
      id: 'binancecoin',
      symbol: 'BNB',
      name: 'BNB',
      current_price: 650 + Math.random() * 100, // $650 - $750 (mais realista)
      market_cap: 100000000000 + Math.random() * 20000000000, // $100B - $120B
      price_change_24h: (Math.random() - 0.5) * 50, // ±$25 variation
      price_change_percentage_24h: (Math.random() - 0.5) * 4, // ±2% variation
      volume_24h: 6000000000 + Math.random() * 3000000000 // $6B - $9B
    },
    {
      id: 'solana',
      symbol: 'SOL',
      name: 'Solana',
      current_price: 200 + Math.random() * 40, // $200 - $240 (mais realista)
      market_cap: 80000000000 + Math.random() * 20000000000, // $80B - $100B
      price_change_24h: (Math.random() - 0.5) * 20, // ±$10 variation
      price_change_percentage_24h: (Math.random() - 0.5) * 6, // ±3% variation
      volume_24h: 5000000000 + Math.random() * 2000000000 // $5B - $7B
    },
    {
      id: 'cardano',
      symbol: 'ADA',
      name: 'Cardano',
      current_price: 0.65 + Math.random() * 0.15, // $0.65 - $0.80 (mais realista)
      market_cap: 25000000000 + Math.random() * 10000000000, // $25B - $35B
      price_change_24h: (Math.random() - 0.5) * 0.1, // ±$0.05 variation
      price_change_percentage_24h: (Math.random() - 0.5) * 5, // ±2.5% variation
      volume_24h: 2000000000 + Math.random() * 1000000000 // $2B - $3B
    },
    {
      id: 'polkadot',
      symbol: 'DOT',
      name: 'Polkadot',
      current_price: 8.5 + Math.random() * 1.5, // $8.5 - $10.0 (mais realista)
      market_cap: 12000000000 + Math.random() * 5000000000, // $12B - $17B
      price_change_24h: (Math.random() - 0.5) * 0.8, // ±$0.4 variation
      price_change_percentage_24h: (Math.random() - 0.5) * 4, // ±2% variation
      volume_24h: 1500000000 + Math.random() * 800000000 // $1.5B - $2.3B
    },
    {
      id: 'chainlink',
      symbol: 'LINK',
      name: 'Chainlink',
      current_price: 18.5 + Math.random() * 3, // $18.5 - $21.5 (mais realista)
      market_cap: 11000000000 + Math.random() * 4000000000, // $11B - $15B
      price_change_24h: (Math.random() - 0.5) * 1.5, // ±$0.75 variation
      price_change_percentage_24h: (Math.random() - 0.5) * 5, // ±2.5% variation
      volume_24h: 1200000000 + Math.random() * 600000000 // $1.2B - $1.8B
    }
  ];
  
  console.log(`🔄 Fallback data generated: ${fallbackCoins.length} cryptocurrencies`);
  console.log(`⚠️  Note: These are simulated values. Real-time data is preferred.`);
  return fallbackCoins;
}

// Obter dados das criptomoedas específicas
function getTargetCryptocurrencies() {
  return new Promise((resolve, reject) => {
    // Primeiro tentar CoinGecko, se falhar, tentar CoinCap
    tryCoinGecko()
      .then(resolve)
      .catch(() => {
        console.log('🔄 CoinGecko failed, trying CoinCap API...');
        return tryCoinCap();
      })
      .then(resolve)
      .catch(reject);
  });
}

// Tentar API CoinGecko
function tryCoinGecko() {
  return new Promise((resolve, reject) => {
    const coinIds = TARGET_CRYPTOCURRENCIES.join(',');
    const url = `https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=${coinIds}&order=market_cap_desc&sparkline=false&price_change_percentage=24h`;
    
    console.log('🔍 Trying CoinGecko API...');
    
    const req = https.get(url, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          if (res.statusCode !== 200) {
            reject(new Error(`CoinGecko HTTP ${res.statusCode}`));
            return;
          }
          
          const jsonData = JSON.parse(data);
          if (jsonData.length === 0) {
            reject(new Error('CoinGecko returned empty data'));
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
          
          console.log(`✅ CoinGecko success: ${result.length} cryptocurrencies`);
          resolve(result);
        } catch (parseError) {
          reject(new Error('CoinGecko parse error'));
        }
      });
    });
    
    req.on('error', () => reject(new Error('CoinGecko connection error')));
    req.setTimeout(8000, () => {
      req.destroy();
      reject(new Error('CoinGecko timeout'));
    });
  });
}

// Tentar API CoinCap (alternativa)
function tryCoinCap() {
  return new Promise((resolve, reject) => {
    // CoinCap usa IDs diferentes, mapear para os símbolos
    const symbols = ['bitcoin', 'ethereum', 'ripple', 'binance-coin', 'solana', 'cardano', 'polkadot', 'chainlink'];
    const url = `https://api.coincap.io/v2/assets?ids=${symbols.join(',')}`;
    
    console.log('🔍 Trying CoinCap API...');
    
    const req = https.get(url, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          if (res.statusCode !== 200) {
            reject(new Error(`CoinCap HTTP ${res.statusCode}`));
            return;
          }
          
          const jsonData = JSON.parse(data);
          if (!jsonData.data || jsonData.data.length === 0) {
            reject(new Error('CoinCap returned empty data'));
            return;
          }

          const result = jsonData.data.map(coin => ({
            id: coin.id,
            symbol: coin.symbol.toUpperCase(),
            name: coin.name,
            current_price: parseFloat(coin.priceUsd),
            market_cap: parseFloat(coin.marketCapUsd),
            price_change_24h: parseFloat(coin.changePercent24Hr),
            price_change_percentage_24h: parseFloat(coin.changePercent24Hr),
            volume_24h: parseFloat(coin.volumeUsd24Hr)
          }));
          
          console.log(`✅ CoinCap success: ${result.length} cryptocurrencies`);
          resolve(result);
        } catch (parseError) {
          reject(new Error('CoinCap parse error'));
        }
      });
    });
    
    req.on('error', () => reject(new Error('CoinCap connection error')));
    req.setTimeout(8000, () => {
      req.destroy();
      reject(new Error('CoinCap timeout'));
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
