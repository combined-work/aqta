function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(tabId).classList.add('active');
}

// Initialize Chart
const ctx = document.getElementById('equityChart').getContext('2d');
const equityChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['09:30', '10:00', '10:30', '11:00', '11:30', '12:00'],
        datasets: [{
            label: 'Portfolio Equity',
            data: [10000, 10050, 10100, 10080, 10150, 10240],
            borderColor: '#3fb950',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: false
            }
        }
    }
});

// WebSocket Connection
const socket = new WebSocket(`ws://${window.location.host}/ws`);

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);
    if (data.type === 'portfolio_tick') {
        document.getElementById('equity-display').innerText = `Equity: $${data.equity.toLocaleString()}`;
        const pnl = data.daily_pnl;
        const pnlPct = data.daily_pnl_pct;
        const pnlEl = document.getElementById('pnl-display');
        pnlEl.innerText = `${pnl >= 0 ? '+' : ''}$${pnl.toLocaleString()} (${pnlPct}%)`;
        pnlEl.className = pnl >= 0 ? 'profit' : 'loss';
    }
};

async function downloadForm8949() {
    window.location.href = '/tax/form8949';
}

// Fetch initial data
async function fetchStrategies() {
    // In a real app, fetch from /strategies
    const strategyList = [
        {id: "EQ-01", name: "Trend Following", status: "HEALTHY", pnl: "+$120"},
        {id: "A1", name: "ORB", status: "HEALTHY", pnl: "+$45"},
        {id: "OP-01", name: "0DTE Condor", status: "HEALTHY", pnl: "-$10"},
        {id: "CR-01", name: "Crypto Trend", status: "HEALTHY", pnl: "+$300"}
    ];
    const tbody = document.getElementById('strategy-list');
    tbody.innerHTML = strategyList.map(s => `
        <tr>
            <td>${s.id}</td>
            <td>${s.name}</td>
            <td>${s.status}</td>
            <td>${s.pnl}</td>
        </tr>
    `).join('');
}

fetchStrategies();
