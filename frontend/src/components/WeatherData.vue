<template>
  <div>
    <h1>Weather Data</h1>

    <input type="text" v-model="searchQuery" @keyup.enter="searchCity" placeholder="Type a city name and press Enter..."
      class="search-input" />

    <div class="table-container">
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
          <tr v-for="city in filteredWeatherData" :key="city.name">
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
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      weatherData: [], // Weather details for predefined cities
      filteredWeatherData: [],
      searchQuery: '',
      cityList: [], // List of predefined cities
      isDataLoaded: false // Track if data is loaded
    };
  },
  mounted() {
    this.fetchWeatherData(); // Fetch weather data for predefined cities
    // Set up an interval to fetch data every 5 minutes
    setInterval(this.fetchWeatherData, 300000); // 300,000 milliseconds = 5 minutes
  },
  methods: {
    async fetchWeatherData() {
      try {
        const response = await axios.get('http://localhost:8000/weather/'); // Adjust this URL to your endpoint
        this.weatherData = response.data;
        this.filteredWeatherData = this.weatherData; // Initialize filtered data
        this.cityList = this.weatherData.map(city => city.name.toLowerCase()); // Populate city list
        this.isDataLoaded = true;
        this.$emit('data-loaded', this.isDataLoaded);
      } catch (error) {
        console.error("Error fetching weather data:", error);
      }
    },
    async searchCity() {
      const query = this.searchQuery;
      if (this.cityList.includes(query)) {
        // If the city is already in the predefined list, show its details
        const existingCity = this.weatherData.find(city => city.name.toLowerCase() === query.toLowerCase());
        this.filteredWeatherData = [existingCity]; // Display the existing city's data
      } else {
        // If the city is not in the list, fetch from backend
        await this.fetchWeatherFromBackend(query);
      }

      this.searchQuery = ''; // Clear search input after fetching
    },
    async fetchWeatherFromBackend(cityName) {
      try {
        const response = await axios.post('http://localhost:8000/search_city_weather/', { city: cityName });

        const newCityData = response.data[0];
        console.log(newCityData);
        // Add new city data to the filteredWeatherData array and update filtered data
        this.filteredWeatherData = [newCityData];

        // Update the city list to include the new city
        this.cityList.push(newCityData.name.toLowerCase());
      } catch (error) {
        console.error("Error fetching weather data from backend:", error);
        alert("City not found. Please check the name and try again.");
      }
    }
  },
};
</script>

<style scoped>
.search-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1em;
}

.table-container {
  max-height: 400px;
  /* Set a max height for scrolling */
  overflow-y: auto;
  /* Enable vertical scrolling */
}

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
