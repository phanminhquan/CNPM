function drawRevenueChart(labels, data) {
const ctx = document.getElementById('revenueStats');

  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: labels,
      datasets: [{
        label: 'Tỉ lệ đạt',
        data: data,
        borderWidth: 1,
        backgroundColor: ['blue', 'rgba(198, 111, 90, 0.8)', 'rgba(255, 199, 120, 0.8)']
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        }
      }
    }
  });
}
