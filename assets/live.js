// CryptoDaily Live Price Updater
// Shared across all pages

const fmtPrice = (n) => {
    if (n == null) return 'N/A';
    if (n >= 1) return '$' + n.toLocaleString('en-US', {minimumFractionDigits:2, maximumFractionDigits:2});
    if (n >= 0.01) return '$' + n.toFixed(4);
    return '$' + n.toFixed(8);
};

async function updateLivePrice() {
    // Update date and time
    const now = new Date();
    const dateEl  = document.getElementById('live-date');
    const timeEl  = document.getElementById('live-time');
    if (dateEl) dateEl.textContent = now.toLocaleDateString('en-US', {month:'long', day:'numeric', year:'numeric'});
    if (timeEl) timeEl.textContent = now.toUTCString().slice(17,22) + ' UTC';

    try {
        const response = await fetch('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_24hr_change=true');
        const data     = await response.json();
        const price    = data.bitcoin.usd;
        const change   = data.bitcoin.usd_24h_change.toFixed(2);
        const arrow    = change >= 0 ? '▲' : '▼';
        const color    = change >= 0 ? '#4caf50' : '#f44336';
        const priceStr = fmtPrice(price);

        // Update top bar
        const livePrice = document.getElementById('live-price');
        if (livePrice) livePrice.innerHTML =
            `BTC: <strong style="color:#f7931a">${priceStr}</strong> <span style="color:${color}">${arrow} ${Math.abs(change)}%</span>`;

        // Update header
        const headerPrice  = document.getElementById('header-price');
        const headerChange = document.getElementById('header-change');
        if (headerPrice)  headerPrice.textContent = priceStr;
        if (headerChange) headerChange.innerHTML  =
            `<span style="color:${color}">${arrow} ${Math.abs(change)}% (24h)</span>`;

    } catch(e) {
        const livePrice = document.getElementById('live-price');
        if (livePrice) livePrice.textContent = 'BTC: Data loading...';
    }
}

// Run immediately then every 60 seconds
updateLivePrice();
setInterval(updateLivePrice, 60000);