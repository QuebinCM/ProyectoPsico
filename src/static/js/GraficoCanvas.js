var ctx = document.getElementById('grafica').getContext('2d');

var data = {
  labels: ['Depresión', 'Ansiedad', 'Estres'],
  datasets: [{
    label: 'Percentiles',
    data: [98, 61, 97],
    backgroundColor: [
        'rgba(112, 224, 0)',
        'rgba(255, 234, 0)',
        'rgba(0, 80, 157)',
    ],
    borderColor: [
        'rgba(112, 224, 0)',
        'rgba(255, 234, 0)',
        'rgba(0, 80, 157)',
    ],
    borderWidth: 1
  }]
};

var options = {
  scales: {
    y: {
      beginAtZero: true,
      max: 100
    }
  }
};

var myChart = new Chart(ctx, {
  type: 'bar',
  data: data,
  options: options
  
});