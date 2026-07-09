const API_BASE_URL = '';

document.addEventListener('DOMContentLoaded', () => {
    const queryInput = document.getElementById('query-input');
    const sendBtn = document.getElementById('send-btn');
    const responseContent = document.getElementById('response-content');
    const statusBadge = document.getElementById('status-badge');
    const refreshMetricsBtn = document.getElementById('refresh-metrics-btn');

    // Meta elements
    const metaModel = document.getElementById('meta-model');
    const metaTokens = document.getElementById('meta-tokens');
    const metaCost = document.getElementById('meta-cost');
    const metaLatency = document.getElementById('meta-latency');
    const metaConfidence = document.getElementById('meta-confidence');
    const metaCached = document.getElementById('meta-cached');

    // Aggregate elements
    const aggTotal = document.getElementById('agg-total');
    const aggCache = document.getElementById('agg-cache');
    const aggTokens = document.getElementById('agg-tokens');
    const aggCost = document.getElementById('agg-cost');

    // Initial metrics fetch
    fetchMetrics();

    sendBtn.addEventListener('click', handleSendQuery);
    
    // Allow submitting with Ctrl+Enter
    queryInput.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            handleSendQuery();
        }
    });

    refreshMetricsBtn.addEventListener('click', fetchMetrics);

    async function handleSendQuery() {
        const query = queryInput.value.trim();
        if (!query) return;

        // Set Loading state
        sendBtn.disabled = true;
        sendBtn.innerHTML = '<span>Processing...</span><i class="fa-solid fa-spinner fa-spin"></i>';
        responseContent.innerHTML = `
            <div class="loader">
                <div class="dot"></div>
                <div class="dot"></div>
                <div class="dot"></div>
            </div>
        `;
        statusBadge.className = 'badge hidden';
        resetMeta();

        try {
            const response = await fetch(`${API_BASE_URL}/route`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ query })
            });

            if (!response.ok) {
                throw new Error(`API Error: ${response.status}`);
            }

            const data = await response.json();
            
            // Display Result
            responseContent.innerHTML = escapeHTML(data.response);
            
            // Update Meta
            metaModel.textContent = data.model_used;
            metaTokens.textContent = data.tokens_used.toLocaleString();
            metaCost.textContent = `$${data.cost.toFixed(6)}`;
            metaLatency.textContent = `${data.latency_ms.toFixed(0)} ms`;
            metaConfidence.textContent = `${(data.confidence * 100).toFixed(1)}%`;
            metaCached.textContent = data.cached ? 'Yes' : 'No';

            // Update Badge
            statusBadge.className = `badge ${data.cached ? 'cached' : ''}`;
            statusBadge.textContent = data.cached ? 'Cache Hit' : 'Success';

            // Fetch metrics silently to update aggregate
            fetchMetrics();

        } catch (error) {
            responseContent.innerHTML = `<p style="color: #ef4444;"><i class="fa-solid fa-circle-exclamation"></i> Error: ${error.message}</p>`;
            statusBadge.className = 'badge error';
            statusBadge.textContent = 'Error';
        } finally {
            sendBtn.disabled = false;
            sendBtn.innerHTML = '<span>Send Query</span><i class="fa-solid fa-paper-plane"></i>';
        }
    }

    async function fetchMetrics() {
        try {
            refreshMetricsBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Refreshing...';
            
            const response = await fetch(`${API_BASE_URL}/metrics`);
            if (!response.ok) throw new Error('Failed to fetch metrics');
            
            const data = await response.json();
            
            aggTotal.textContent = data.total_requests.toLocaleString();
            aggCache.textContent = data.cache_hits.toLocaleString();
            aggTokens.textContent = data.total_tokens_used.toLocaleString();
            aggCost.textContent = `$${data.total_cost.toFixed(4)}`;
        } catch (error) {
            console.error('Error fetching metrics:', error);
        } finally {
            refreshMetricsBtn.innerHTML = '<i class="fa-solid fa-arrows-rotate"></i> Refresh Metrics';
        }
    }

    function resetMeta() {
        metaModel.textContent = '-';
        metaTokens.textContent = '-';
        metaCost.textContent = '-';
        metaLatency.textContent = '-';
        metaConfidence.textContent = '-';
        metaCached.textContent = '-';
    }

    // Helper to escape HTML to prevent XSS
    function escapeHTML(str) {
        return str
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;')
            .replace(/'/g, '&#039;');
    }
});
