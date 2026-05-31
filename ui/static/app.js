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
    console.log("WS Data:", data);
};

// Fetch initial data
async function fetchStrategies() {
    // In a real app, fetch from /strategies
    const strategyList = [
        {id: "EQ-01", name: "Trend Following", status: "HEALTHY", pnl: "+$120"},
        {id: "A1", name: "ORB", status: "HEALTHY", pnl: "+$45"}
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
