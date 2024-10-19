<!-- src/App.vue -->
<template>
    <div id="app">
      <h1>Weather Monitoring Dashboard</h1>
  
      <!-- WeatherData Component -->
      <WeatherData @weather-data-loaded="onWeatherDataLoaded" />
  
      <!-- DailyAggregates Component (display only after weather data is loaded) -->
      <DailyAggregates v-if="showDailyAggregates" />
    </div>
  </template>
  
  <script>
  import WeatherData from './components/WeatherData.vue';
  import DailyAggregates from './components/DailyAggregates.vue';
  
  export default {
    components: {
      WeatherData,
      DailyAggregates,
    },
    data() {
      return {
        showDailyAggregates: false,  // Initially, daily aggregates won't be shown
      };
    },
    methods: {
      onWeatherDataLoaded() {
        // Once the weather data is loaded, show the daily aggregates component
        this.showDailyAggregates = true;
      },
    },
  };
  </script>
  
  <style>
  /* Global styles here */
  #app {
    margin: 20px;
  }
  
  h1 {
    color: #444;
    margin-bottom: 20px;
  }
  </style>
  