const https = require('https');

// Teste da API do CoinGecko
function testCoinGeckoAPI() {
  return new Promise((resolve, reject) => {
    const coinIds = 'bitcoin,ethereum,ripple,binancecoin,solana';
    const url = `https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=${coinIds}&order=market_cap_desc&sparkline=false&price_change_percentage=24h`;
    
    console.log('🔍 Testing CoinGecko API...');
    console.log('URL:', url);
    
    const req = https.get(url, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          console.log(`\n📡 API Response: ${res.statusCode} ${res.statusMessage}`);
          
          if (res.statusCode !== 200) {
            console.error(`❌ API Error: HTTP ${res.statusCode}`);
            console.error('Response:', data);
            reject(new Error(`HTTP ${res.statusCode}`));
            return;
          }
          
          const jsonData = JSON.parse(data);
          console.log(`✅ Success! Received ${jsonData.length} cryptocurrencies`);
          
          // Mostrar dados reais
          jsonData.forEach((coin, index) => {
            console.log(`\n${index + 1}. ${coin.name} (${coin.symbol.toUpperCase()})`);
            console.log(`   💰 Current Price: $${coin.current_price}`);
            console.log(`   📈 24h Change: ${coin.price_change_percentage_24h}%`);
            console.log(`   💎 Market Cap: $${(coin.market_cap / 1000000000).toFixed(2)}B`);
            console.log(`   📊 Volume: $${(coin.total_volume / 1000000000).toFixed(2)}B`);
          });
          
          resolve(jsonData);
        } catch (parseError) {
          console.error('❌ Parse Error:', parseError.message);
          console.error('Raw response:', data);
          reject(parseError);
        }
      });
    });
    
    req.on('error', (err) => {
      console.error('❌ Request Error:', err.message);
      reject(err);
    });
    
    req.setTimeout(10000, () => {
      console.error('⏰ Timeout after 10 seconds');
      req.destroy();
      reject(new Error('Timeout'));
    });
  });
}

// Executar teste
console.log('🚀 Starting CoinGecko API Test...\n');

testCoinGeckoAPI()
  .then(data => {
    console.log('\n🎉 API Test Successful!');
    console.log(`Total cryptocurrencies received: ${data.length}`);
  })
  .catch(error => {
    console.error('\n💥 API Test Failed:', error.message);
    process.exit(1);
  });
