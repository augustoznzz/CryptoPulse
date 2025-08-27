// Crypto Trading Analyzer - Frontend JavaScript (Versão Estática para Netlify)

document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('searchBtn');
    const buttonText = document.querySelector('.button-text');
    const loadingSpinner = document.querySelector('.loading-spinner');
    const resultsSection = document.getElementById('results');
    const resultsContainer = document.getElementById('resultsContainer');
    const analysisInfo = document.getElementById('analysisInfo');
    const errorSection = document.getElementById('error');
    const errorMessage = document.getElementById('errorMessage');

    searchBtn.addEventListener('click', function() {
        startSearch();
    });

    function startSearch() {
        // Disable button and show loading
        searchBtn.disabled = true;
        buttonText.style.opacity = '0';
        loadingSpinner.style.display = 'block';
        
        // Hide previous results/errors
        resultsSection.style.display = 'none';
        errorSection.style.display = 'none';

        // Simulate API call delay for demo purposes
        setTimeout(() => {
            // Generate demo data
            const demoData = generateDemoData();
            displayResults(demoData);
            
            // Re-enable button
            searchBtn.disabled = false;
            buttonText.style.opacity = '1';
            loadingSpinner.style.display = 'none';
        }, 2000); // 2 second delay to simulate processing
    }

    function generateDemoData() {
        const cryptoList = ['BTC', 'ETH', 'BNB', 'ADA', 'SOL', 'DOT', 'AVAX', 'MATIC', 'LINK', 'UNI'];
        const results = [];
        
        // Generate 3-5 random results
        const numResults = Math.floor(Math.random() * 3) + 3;
        
        for (let i = 0; i < numResults; i++) {
            const symbol = cryptoList[Math.floor(Math.random() * cryptoList.length)];
            const type = Math.random() > 0.5 ? 'LONG' : 'SHORT';
            const potentialGain = (Math.random() * 15 + 5).toFixed(1);
            
            const signal = generateSignalText(symbol, type, potentialGain);
            
            results.push({
                symbol: symbol,
                type: type,
                potential_gain: potentialGain,
                signal: signal
            });
        }
        
        // Sort by potential gain
        results.sort((a, b) => parseFloat(b.potential_gain) - parseFloat(a.potential_gain));
        
        return {
            success: true,
            results: results,
            total_analyzed: 50,
            timestamp: new Date().toLocaleString('pt-BR')
        };
    }

    function generateSignalText(symbol, type, gain) {
        const indicators = [
            'RSI: Sobrecomprado (70+)',
            'MACD: Cruzamento de alta',
            'Média Móvel: Preço acima da MA200',
            'Volume: Aumento de 25%',
            'Suporte: Testado e mantido',
            'Resistência: Próximo breakout',
            'Momentum: Forte tendência de alta',
            'Divergência: RSI vs Preço'
        ];
        
        const selectedIndicators = indicators
            .sort(() => 0.5 - Math.random())
            .slice(0, 4);
        
        return `Análise Técnica ${symbol}:\n` +
               `• ${selectedIndicators[0]}\n` +
               `• ${selectedIndicators[1]}\n` +
               `• ${selectedIndicators[2]}\n` +
               `• ${selectedIndicators[3]}\n\n` +
               `Estratégia: ${type === 'LONG' ? 'Compra' : 'Venda'} com alvo +${gain}%`;
    }

    function displayResults(data) {
        resultsContainer.innerHTML = '';
        
        if (data.results && data.results.length > 0) {
            data.results.forEach((result, index) => {
                const card = createTradeCard(result, index + 1);
                resultsContainer.appendChild(card);
            });

            // Show analysis info
            analysisInfo.innerHTML = `
                <p><strong>Análise completa:</strong> ${data.total_analyzed} criptomoedas analisadas</p>
                <p><strong>Timestamp:</strong> ${data.timestamp}</p>
                <p><strong>Melhores oportunidades:</strong> Top ${data.results.length} selecionadas</p>
                <p><em>💡 Esta é uma demonstração estática. Em produção, os dados viriam de análise em tempo real.</em></p>
            `;

            resultsSection.style.display = 'block';
        } else {
            displayError('Nenhuma oportunidade de trading encontrada no momento.');
        }
    }

    function createTradeCard(result, rank) {
        const card = document.createElement('div');
        card.className = 'trade-card';
        
        const signalTypeClass = result.type === 'LONG' ? 'signal-long' : 'signal-short';
        const emoji = result.type === 'LONG' ? '🔼' : '🔽';
        
        card.innerHTML = `
            <div class="card-header">
                <div class="crypto-symbol">#${rank} ${result.symbol}/USDT</div>
                <div class="signal-type ${signalTypeClass}">${emoji} ${result.type}</div>
            </div>
            <div class="potential-gain">
                Potencial: +${result.potential_gain}%
            </div>
            <div class="trade-details">${result.signal}</div>
        `;
        
        return card;
    }

    function displayError(message) {
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
    }

    // Add some visual feedback for button interactions
    searchBtn.addEventListener('mouseenter', function() {
        if (!this.disabled) {
            this.style.transform = 'translateY(-2px)';
        }
    });

    searchBtn.addEventListener('mouseleave', function() {
        if (!this.disabled) {
            this.style.transform = 'translateY(0)';
        }
    });
});

// Add a subtle parallax effect to the background
document.addEventListener('mousemove', function(e) {
    const moveX = (e.clientX * -1 / 150);
    const moveY = (e.clientY * -1 / 150);
    
    document.body.style.backgroundPosition = `${moveX}px ${moveY}px`;
});

// Add keyboard shortcut (Space or Enter) to trigger search
document.addEventListener('keydown', function(e) {
    if ((e.code === 'Space' || e.code === 'Enter') && !document.getElementById('searchBtn').disabled) {
        e.preventDefault();
        document.getElementById('searchBtn').click();
    }
});