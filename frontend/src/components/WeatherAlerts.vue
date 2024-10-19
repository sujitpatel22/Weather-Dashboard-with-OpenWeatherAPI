<template>
  <div class="weather-alerts">

    <h2 class="title">Set Weather Alert Thresholds</h2>
    <form @submit.prevent="saveThresholds" class="form-container">
      <div class="form-group">
        <label for="city">City</label>
        <input v-model="city" id="city" placeholder="Enter city" required />
      </div>

      <div class="form-group">
        <label for="temp_threshold">Temperature Threshold (°C)</label>
        <input type="number" v-model="temp_threshold" id="temp_threshold" placeholder="Enter temperature threshold" />
      </div>

      <div class="form-group">
        <label for="wind_speed_threshold">Wind Speed Threshold (m/s)</label>
        <input type="number" v-model="wind_speed_threshold" id="wind_speed_threshold"
          placeholder="Enter wind speed threshold" />
      </div>

      <div class="form-group">
        <label for="humidity_threshold">Humidity Threshold (%)</label>
        <input type="number" v-model="humidity_threshold" id="humidity_threshold"
          placeholder="Enter humidity threshold" />
      </div>

      <div class="form-group">
        <label for="consecutive_updates">Consecutive Updates</label>
        <input type="number" v-model="consecutive_updates" id="consecutive_updates" min="1"
          placeholder="Number of consecutive updates" />
      </div>
      <div class='form-group'>
        <button type="submit" class="btn-save">Save Thresholds</button>
      </div>
    </form>

    <div v-if="message" class="alert">{{ message }}</div>

    <h2 class="title">Weather Alerts</h2>
    <button @click="checkWeatherAlerts" class="btn-alerts">Check Weather Alerts</button>

    <div v-if="alerts.length" class="alerts-container">
      <h3 class="sub-title">Alerts:</h3>
      <ul>
        <li v-for="alert in alerts" :key="alert" class="alert-item">{{ alert }}</li>
      </ul>
    </div>
    <div v-else class="no-alerts-message">
      <p>No alerts found.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      city: '',
      temp_threshold: null,
      wind_speed_threshold: null,
      humidity_threshold: null,
      consecutive_updates: 2,
      message: '',
      alerts: []
    };
  },
  methods: {
    getCSRFToken() {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; csrftoken=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
      return null;  // Return null if no CSRF token is found
    },

    saveThresholds() {
      const thresholdData = {
        city: this.city,
        temp_threshold: this.temp_threshold,
        wind_speed_threshold: this.wind_speed_threshold,
        humidity_threshold: this.humidity_threshold,
        consecutive_updates: this.consecutive_updates
      };

      const csrfToken = this.getCSRFToken();

      axios.post('http://localhost:8000/save_thresholds/', thresholdData, {
        headers: {
          'X-CSRFToken': csrfToken,
        },
        withCredentials: true,
      })
        .then(response => {
          this.message = response.data.message || 'Thresholds saved successfully';
        })
        .catch(error => {
          console.error('Error saving thresholds:', error);
          this.message = 'Error saving thresholds';
        });
    },
    checkWeatherAlerts() {
      axios.get('http://localhost:8000/check_alerts/')
        .then(response => {
          this.alerts = response.data.alerts || [];
        })
        .catch(error => {
          console.error('Error fetching alerts:', error);
          this.alerts = [];
        });
    },
  }
};
</script>

<style scoped>
.weather-alerts {
  margin: 20px auto;
  max-width: 100%;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 1.5em;
  color: #333;
}

.form-container {
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  gap: 15px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

label {
  font-weight: bold;
  margin-bottom: 5px;
  color: #555;
}

input {
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1em;
}

input:focus {
  outline: none;
  border-color: #4CAF50;
}

.btn-save {
  background-color: #4CAF50;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
  font-size: 1.1em;
  border-radius: 4px;
  transition: background-color 0.3s ease;
}

.btn-save:hover {
  background-color: #45a049;
}

.alert {
  margin-top: 20px;
  color: green;
  text-align: center;
}

.btn-alerts {
  background-color: #2196F3;
  color: white;
  padding: 10px;
  border: none;
  cursor: pointer;
  font-size: 1.1em;
  border-radius: 4px;
  transition: background-color 0.3s ease;
  display: block;
  margin: 20px auto;
}

.btn-alerts:hover {
  background-color: #1e88e5;
}

.alerts-container {
  margin-top: 20px;
  padding: 15px;
  background-color: #fff3e0;
  border: 1px solid #ffe0b2;
  border-radius: 8px;
}

.sub-title {
  text-align: center;
  margin-bottom: 10px;
  font-size: 1.2em;
}

.alert-item {
  background-color: #ffcdd2;
  padding: 10px;
  margin-bottom: 5px;
  border-radius: 4px;
  list-style: none;
}

.no-alerts-message {
  margin-top: 20px;
  text-align: center;
  font-size: 1.1em;
  color: #888;
}
</style>
