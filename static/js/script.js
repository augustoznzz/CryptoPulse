// Crypto Trading Analyzer - Frontend JavaScript

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

        // Make API call with longer timeout
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 300000); // 5 minutes timeout
        
        fetch('/api/search-trades', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            signal: controller.signal
        })
        .then(response => {
            clearTimeout(timeoutId);
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
            clearTimeout(timeoutId);
            console.error('Error:', error);
            if (error.name === 'AbortError') {
                displayError('Análise demorou muito tempo. Tente novamente.');
            } else if (error.message.includes('HTTP')) {
                displayError(`Erro do servidor: ${error.message}`);
            } else {
                displayError('Erro de conexão. Tente novamente.');
            }
        })
        .finally(() => {
            // Re-enable button
            searchBtn.disabled = false;
            buttonText.style.opacity = '1';
            loadingSpinner.style.display = 'none';
        });
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