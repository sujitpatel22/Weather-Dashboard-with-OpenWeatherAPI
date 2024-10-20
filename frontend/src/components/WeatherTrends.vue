<template>
  <div class="weather-trends">
    <h1 class="trends-title">Weather Trends</h1>

    <div class='trend-config-container'>
      <div class="city-select">
        <label for="city">Select City:</label>
        <select v-model="selectedCity">
          <option v-for="city in cities" :key="city.id" :value="city.city">
            {{ city.city }}
          </option>
        </select>
      </div>

      <div class="time-frame-select">
        <label for="time-frame">Select Time Frame:</label>
        <select v-model="selectedTimeFrame" @change="fetchWeatherTrends">
          <option value="1_week">1 Week</option>
          <option value="15_days">15 Days</option>
          <option value="30_days">30 Days</option>
          <option value="2_months">2 Months</option>
          <option value="6_months">6 Months</option>
        </select>
      </div>
    </div>

    <div v-if="weatherTrends" class="charts-container">
      <v-chart :option="avgTempChartOptions" class="line-chart" />
      <v-chart :option="maxTempChartOptions" class="line-chart" />
      <v-chart :option="minTempChartOptions" class="line-chart" />
      <v-chart :option="avgHumidityChartOptions" class="line-chart" />
      <v-chart :option="avgWindSpeedChartOptions" class="line-chart" />
    </div>

    <div v-else>
      <p>Select a city and time frame to view trends.</p>
    </div>
  </div>
</template>

<script>
import { use } from 'echarts/core';
import ECharts from 'vue-echarts';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart } from 'echarts/charts';
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components';
import axios from 'axios';

use([
  CanvasRenderer,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
]);

export default {
  components: {
    'v-chart': ECharts,
  },
  data() {
    return {
      cities: [],
      selectedCity: null,
      selectedTimeFrame: '1_week',
      weatherTrends: null,
      avgTempChartOptions: null,
      maxTempChartOptions: null,
      minTempChartOptions: null,
      avgHumidityChartOptions: null,
      avgWindSpeedChartOptions: null,
    };
  },
  mounted() {
    this.fetchCities();
  },
  methods: {
    async fetchCities() {
      try {
        const response = await axios.get('http://localhost:8000/get_cities/');
        this.cities = response.data;
        this.selectedCity = this.cities[0].city;  // Default to the first city
        this.fetchWeatherTrends();                 // Fetch trends for the default city
      } catch (error) {
        console.error('Error fetching cities:', error);
      }
    },
    async fetchWeatherTrends() {
      if (!this.selectedCity) return;

      try {
        const response = await axios.get(`http://localhost:8000/get_trends/${this.selectedCity}/${this.selectedTimeFrame}/`);
        this.weatherTrends = response.data;

        // Prepare chart options
        this.avgTempChartOptions = this.prepareChartOptions('Average Temperature (°C)', this.weatherTrends.dates, this.weatherTrends.avg_temp);
        this.maxTempChartOptions = this.prepareChartOptions('Max Temperature (°C)', this.weatherTrends.dates, this.weatherTrends.max_temp);
        this.minTempChartOptions = this.prepareChartOptions('Min Temperature (°C)', this.weatherTrends.dates, this.weatherTrends.min_temp);
        this.avgHumidityChartOptions = this.prepareChartOptions('Average Humidity (%)', this.weatherTrends.dates, this.weatherTrends.avg_humidity);
        this.avgWindSpeedChartOptions = this.prepareChartOptions('Average Wind Speed (m/s)', this.weatherTrends.dates, this.weatherTrends.avg_wind_speed);
      } catch (error) {
        console.error('Error fetching weather trends:', error);
      }
    },
    prepareChartOptions(label, dates, data) {
      return {
        title: {
          text: label,
          left: 'center',
        },
        tooltip: {
          trigger: 'axis',
        },
        xAxis: {
          type: 'category',
          data: dates,
        },
        yAxis: {
          type: 'value',
        },
        series: [
          {
            name: label,
            type: 'line',
            data: data,
            smooth: true,
            lineStyle: {
              width: 2,
              color: '#42b983',
            },
          },
        ],
      };
    },
  },
};
</script>

<style scoped>
.weather-trends {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px auto;
  padding: 20px;
  max-width: 1200px;
  background-color: #f8f9fa;
  border-radius: 12px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}

.trends-title {
  font-size: 2.5em;
  font-weight: bold;
  margin-bottom: 30px;
  color: #333;
  text-align: center;
  font-family: 'Poppins', sans-serif;
}

.trend-config-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  width: 100%;
  max-width: 800px;
}

.city-select,
.time-frame-select {
  display: flex;
  flex-direction: column;
  align-items: start;
  margin-right: 20px;
}

label {
  font-size: 1.2em;
  color: #555;
  margin-bottom: 8px;
  font-family: 'Roboto', sans-serif;
}

select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1em;
  background-color: #fff;
  color: #333;
  font-family: 'Roboto', sans-serif;
  transition: all 0.3s ease;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
}

select:focus {
  outline: none;
  border-color: #007bff;
  box-shadow: 0px 0px 8px rgba(0, 123, 255, 0.3);
}

.charts-container {
  display: grid;
  grid-template-columns: 1fr;
  grid-gap: 30px;
  width: 100%;
  max-width: 1000px;
}

@media (min-width: 768px) {
  .charts-container {
    grid-template-columns: 1fr 1fr;
  }
}

@media (min-width: 1200px) {
  .charts-container {
    grid-template-columns: repeat(3, 1fr);
  }
}

.line-chart {
  height: 300px;
  position: relative;
  background-color: #fff;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.05);
}
</style>
