<template>
    <div>
      <h1>Weather Data</h1>
      <table class="weather-table">
        <thead>
          <tr>
            <th>City</th>
            <th>Main Condition</th>
            <th>Temperature (°C)</th>
            <th>Feels Like (°C)</th>
            <th>Humidity (%)</th>
            <th>Wind Speed (m/s)</th>
            <th>Last Update</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="city in weatherData" :key="city.name">
            <td>{{ city.name }}</td>
            <td>{{ city.mainCondition }}</td>
            <td>{{ city.temperature.toFixed(2) }}</td>
            <td>{{ city.feelsLike.toFixed(2) }}</td>
            <td>{{ city.humidity }}</td>
            <td>{{ city.windSpeed }}</td>
            <td>{{ new Date(city.lastUpdate * 1000).toLocaleString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        weatherData: [],
      };
    },
    mounted() {
      this.fetchWeatherData();
      // Set up an interval to fetch data every 5 minutes
      setInterval(this.fetchWeatherData, 300000); // 300,000 milliseconds = 5 minutes
    },
    methods: {
      async fetchWeatherData() {
        try {
          const response = await axios.get('http://localhost:8000/weather/');
          this.weatherData = response.data;
        } catch (error) {
          console.error("Error fetching weather data:", error);
        }
      },
    },
  };
  </script>
  
  <style scoped>
  .weather-table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 1.2em;
    text-align: left;
  }
  
  .weather-table thead tr {
    background-color: #4CAF50;
    color: white;
  }
  
  .weather-table th,
  .weather-table td {
    padding: 12px 15px;
    border: 1px solid #ddd;
  }
  
  .weather-table tbody tr {
    transition: background-color 0.3s ease;
  }
  
  .weather-table tbody tr:nth-child(even) {
    background-color: #f2f2f2;
  }
  
  .weather-table tbody tr:hover {
    background-color: #d1e7dd;
  }
  </style>
  