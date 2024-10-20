<template>
  <div class="weather-dashboard">
    <h1 class="dashboard-title">Weather Summary for Today</h1>

    <!-- City Dropdown -->
    <div class="city-select">
      <label for="city">Select City:</label>
      <select v-model="selectedCity">
        <option v-for="city in cities" :key="city.id" :value="city.city">
          {{ city.city }}
        </option>
      </select>
    </div>

    <!-- Weather Cards -->
    <div v-if="weatherData" class="cards-container">
      <div class="card">
        <h3>Average Temperature</h3>
        <p>{{ weatherData.avg_temp }} °C</p>
      </div>
      <div class="card">
        <h3>Max Temperature</h3>
        <p>{{ weatherData.max_temp }} °C</p>
      </div>
      <div class="card">
        <h3>Min Temperature</h3>
        <p>{{ weatherData.min_temp }} °C</p>
      </div>
      <div class="card">
        <h3>Average Humidity</h3>
        <p>{{ weatherData.avg_humidity }} %</p>
      </div>
      <div class="card">
        <h3>Average Wind Speed</h3>
        <p>{{ weatherData.avg_wind_speed }} m/s</p>
      </div>
    </div>

    <div v-else>
      <p>Loading weather data...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      cities: [],
      selectedCity: null,
      weatherData: null,
      loading: null,
      error: null,
    };
  },
  mounted() {
    this.fetchCitiesWithRetry(3);  // Retry logic for fetching cities
    this.startAutoUpdate();        // Auto-update every 5 minutes
  },
  watch: {
    selectedCity(newCity) {
      if (newCity) {
        this.fetchWeatherData();   // Fetch weather data when the city changes
      }
    }
  },
  methods: {
    async fetchCitiesWithRetry(retryCount = 3) {
      try {
        const response = await axios.get('http://localhost:8000/get_cities/');
        if (response.data.length > 0) {
          this.cities = response.data;
          this.selectedCity = this.cities[0].city;  // Default to first city
          this.fetchWeatherData();                // Fetch weather data
        } else if (retryCount > 0) {
          console.log(`Retrying... ${retryCount}`);
          setTimeout(() => this.fetchCitiesWithRetry(retryCount - 1), 3000);
        } else {
          console.log('No cities available after retries');
        }
      } catch (error) {
        console.error('Error fetching cities:', error);
      }
    },
    async fetchWeatherData() {
      if (!this.selectedCity) return;

      try {
        const response = await axios.get(`http://localhost:8000/get_summary/${this.selectedCity}/`);
        const data = response.data;
        console.log(data);
        if (data.error) {
          console.error(data.error);
          return;
        }

        this.weatherData = data;
      } catch (error) {
        console.error('Error fetching weather data:', error);
      }
    },
    startAutoUpdate() {
      setInterval(() => {
        if (this.selectedCity) {
          this.fetchWeatherData();  // Fetch weather data every 5 minutes
        }
      }, 300000);  // 5 minutes = 300000 ms
    }
  }
}
</script>

<style scoped>
.weather-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background: #f7f9fc;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.dashboard-title {
  text-align: center;
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 2rem;
}

.city-select {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 2rem;
}

.city-select label {
  font-size: 1.2rem;
  margin-right: 1rem;
  color: #444;
}

.city-select select {
  padding: 0.5rem 1rem;
  font-size: 1rem;
  border-radius: 5px;
  border: 1px solid #ccc;
  background: #fff;
  color: #333;
}

.cards-container {
  display: flex;
  gap: 2rem;
  justify-content: center;
  flex-direction: row;
  align-items: center;
}

.card {
  background: #fff;
  border-radius: 8px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  text-align: center;
  flex: 1 1 200px;
  /* Responsive sizing */
}

.card h3 {
  margin: 0 0 0.5rem;
  font-size: 1.5rem;
  color: #333;
}

.card p {
  font-size: 1.25rem;
  color: #555;
}
</style>
