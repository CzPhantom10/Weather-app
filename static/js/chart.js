// Chart.js will be loaded via CDN in the template. This file is for custom chart logic if needed.
// Example: window.renderTempChart(labels, data)
window.renderTempChart = function(labels, data) {
  const ctx = document.getElementById('tempChart').getContext('2d');
  if(window.tempChartInstance) window.tempChartInstance.destroy();
  window.tempChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [{
        label: 'Temperature',
        data: data,
        borderColor: '#2196f3',
        backgroundColor: 'rgba(33,150,243,0.08)',
        fill: true,
        tension: 0.4,
        pointRadius: 5,
        pointBackgroundColor: '#2196f3',
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: {
        y: { beginAtZero: false, grid: { color: '#eee' } },
        x: { grid: { color: '#eee' } }
      }
    }
  });
}
