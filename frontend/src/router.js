// src/router.js

import Vue from 'vue';
import Router from 'vue-router';
import WeatherData from './components/WeatherData.vue';
import SetThreshold from './components/SetThreshold.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'WeatherData',
      component: WeatherData,
    },
    {
      path: '/set-threshold',
      name: 'SetThreshold',
      component: SetThreshold,
    },
  ],
});
