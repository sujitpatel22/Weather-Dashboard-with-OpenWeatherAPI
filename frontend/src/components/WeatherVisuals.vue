<template>
    <div class="weather-visualizations">
      <h2>Weather Visualizations</h2>
      <div class="controls">
        <label for="period">Select Period: </label>
        <select v-model="selectedPeriod" @change="fetchWeatherData">
          <option value="1_week">1 Week</option>
          <option value="10_days">10 Days</option>
          <option value="1_month">1 Month</option>
          <option value="2_months">2 Months</option>
          <option value="6_months">6 Months</option>
        </select>
      </div>
  
      <div v-if="weatherData.length > 0">
        <canvas id="weatherChart"></canvas>
      </div>
      <div v-else>
        <p>No data available for the selected period.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { Chart, registerables } from 'chart.js';
  
  Chart.register(...registerables);
  
  export default {
    data() {
      return {
        selectedPeriod: '1_week',
        weatherData: [],
        chart: null,
      };
    },
    methods: {
      fetchWeatherData() {
        axios.get(`http://localhost:8000/weather_visuals/${this.selectedPeriod}`)
          .then(response => {
            this.weatherData = response.data;
            this.renderChart();
          })
          .catch(error => {
            console.error('Error fetching weather data:', error);
          });
      },
      renderChart() {
        const labels = this.weatherData.map(data => data.date);
        const avgTempData = this.weatherData.map(data => data.avg_temp);
        const maxTempData = this.weatherData.map(data => data.max_temp);
        const minTempData = this.weatherData.map(data => data.min_temp);
  
        if (this.chart) {
          this.chart.destroy();  // Destroy the previous chart before creating a new one
        }
  
        const ctx = document.getElementById('weatherChart').getContext('2d');
        this.chart = new Chart(ctx, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [
              {
                label: 'Avg Temp (°C)',
                data: avgTempData,
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false,
                tension: 0.1,
              },
              {
                label: 'Max Temp (°C)',
                data: maxTempData,
                borderColor: 'rgba(255, 99, 132, 1)',
                fill: false,
                tension: 0.1,
              },
              {
                label: 'Min Temp (°C)',
                data: minTempData,
                borderColor: 'rgba(54, 162, 235, 1)',
                fill: false,
                tension: 0.1,
              }
            ]
          },
          options: {
            scales: {
              x: {
                type: 'time',
                time: {
                  unit: 'day',
                  tooltipFormat: 'MMM DD'
                }
              },
              y: {
                beginAtZero: true
              }
            },
            responsive: true,
            plugins: {
              legend: {
                position: 'top',
              },
              tooltip: {
                callbacks: {
                  label: function(tooltipItem) {
                    return `${tooltipItem.dataset.label}: ${tooltipItem.raw.toFixed(2)}°C`;
                  }
                }
              }
            }
          }
        });
      }
    },
    mounted() {
      this.fetchWeatherData();  // Fetch initial data for the default selected period
    }
  };
  </script>
  
  <style scoped>
  .weather-visualizations {
    max-width: 800px;
    margin: 20px auto;
    text-align: center;
  }
  
  .controls {
    margin-bottom: 20px;
  }
  
  canvas {
    max-width: 100%;
    height: 400px;
  }
  
  select {
    padding: 10px;
    font-size: 1em;
    margin-left: 10px;
  }
  </style>
  