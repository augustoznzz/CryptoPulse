// Crypto Trading Analyzer - Frontend JavaScript (Análise das 16 Criptomoedas Selecionadas)

document.addEventListener('DOMContentLoaded', function() {
    const searchBtn = document.getElementById('searchBtn');
    const buttonText = document.querySelector('.button-text');
    const loadingSpinner = document.querySelector('.loading-spinner');
    const resultsSection = document.getElementById('results');
    const resultsContainer = document.getElementById('resultsContainer');
    const analysisInfo = document.getElementById('analysisInfo');
    const errorSection = document.getElementById('error');
    const errorMessage = document.getElementById('errorMessage');

    // Ensure dark background is maintained
    function ensureDarkBackground() {
        document.documentElement.style.background = 'linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 100%)';
        document.body.style.background = 'linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 100%)';
        
        // Force all main containers to have transparent background
        const containers = document.querySelectorAll('.container, .results-section, .results-container, main');
        containers.forEach(container => {
            container.style.background = 'transparent';
        });
    }

    // Call on load and after results display
    ensureDarkBackground();

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

        // Chamar função real da Netlify para análise das criptomoedas selecionadas
        fetch('/.netlify/functions/analyze-crypto', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                displayResults(data);
            } else {
                displayError(data.error || 'Erro desconhecido na análise');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            if (error.message.includes('HTTP')) {
                displayError(`Erro do servidor: ${error.message}`);
            } else {
                displayError('Erro de conexão. Verifique sua internet e tente novamente.');
            }
        })
        .finally(() => {
            // Re-enable button
            searchBtn.disabled = false;
            buttonText.style.opacity = '1';
            loadingSpinner.style.display = 'none';
        });
    }

    // Funções demo removidas - agora usando análise real da Netlify

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
                <p><em>💡 Análise técnica em tempo real com dados reais do mercado</em></p>
            `;

            resultsSection.style.display = 'block';
            
            // Ensure dark background after results are displayed
            setTimeout(ensureDarkBackground, 100);
        } else {
            displayError('Nenhuma oportunidade de trading encontrada no momento.');
        }
    }

    function createTradeCard(result, rank) {
        const card = document.createElement('div');
        card.className = 'trade-card';
        
        const signalTypeClass = result.type === 'LONG' ? 'signal-long' : 'signal-short';
        const emoji = result.type === 'LONG' ? '🔼' : '🔽';
        
        // Adicionar informações de preço e variação se disponíveis
        const priceInfo = result.current_price ? `
            <div style="margin-bottom: 1rem; font-size: 0.9rem; color: #a0a0a0;">
                <span style="color: #ffffff; font-weight: 600;">$${result.current_price.toFixed(4)}</span>
                <span style="margin-left: 1rem; padding: 0.3rem 0.6rem; border-radius: 6px; font-weight: 600; ${result.price_change_24h >= 0 ? 'background: rgba(0, 255, 157, 0.2); color: #00ff9d;' : 'background: rgba(255, 82, 82, 0.2); color: #ff5252;'}">
                    ${result.price_change_24h >= 0 ? '+' : ''}${result.price_change_24h ? result.price_change_24h.toFixed(2) : '0.00'}%
                </span>
            </div>
        ` : '';
        
        // Adicionar barra de confiança se disponível
        const confidenceBar = result.score ? `
            <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem;">
                <span style="font-size: 0.9rem; color: #00ff9d; font-weight: 600; min-width: 60px;">${Math.round(result.score * 100)}%</span>
                <div style="flex: 1; height: 8px; background: rgba(255, 255, 255, 0.1); border-radius: 4px; overflow: hidden;">
                    <div style="height: 100%; background: linear-gradient(135deg, #00ff9d 0%, #00b8ff 100%); width: ${Math.round(result.score * 100)}%; transition: width 0.3s ease;"></div>
                </div>
            </div>
        ` : '';
        
        card.innerHTML = `
            <div class="card-header">
                <div class="crypto-symbol">#${rank} ${result.symbol}/USDT</div>
                <div class="signal-type ${signalTypeClass}">${emoji} ${result.type}</div>
            </div>
            ${priceInfo}
            <div class="potential-gain">
                Potencial: +${result.potential_gain}%
            </div>
            ${confidenceBar}
            <div class="trade-details">${result.signal}</div>
        `;
        
        return card;
    }

    function displayError(message) {
        errorMessage.textContent = message;
        errorSection.style.display = 'block';
        
        // Ensure dark background after error display
        setTimeout(ensureDarkBackground, 100);
    }
    
    // Ensure dark background on window resize
    window.addEventListener('resize', ensureDarkBackground);
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