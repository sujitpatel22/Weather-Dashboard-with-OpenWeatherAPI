<!-- src/App.vue -->

<template>
  <div id="app">
    <header>
      <h1>Weather Monitoring System</h1>
    </header>
    <main>
      <WeatherData />
      <!-- <WeatherVisuals /> -->
      <WeatherAlerts />
    </main>
  </div>
</template>

<script>
import WeatherData from './components/WeatherData.vue';
import WeatherAlerts from "./components/WeatherAlerts.vue";
// import WeatherVisuals from "./components/WeatherVisuals.vue";

export default {
  name: 'App',
  components: {
    WeatherData,
    // WeatherVisuals,
    WeatherAlerts
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

header {
  background-color: #4CAF50;
  color: white;
  padding: 10px;
}

main {
  padding: 20px;
}

footer {
  margin-top: 20px;
  font-size: 0.9em;
  color: #666;
}
</style>
