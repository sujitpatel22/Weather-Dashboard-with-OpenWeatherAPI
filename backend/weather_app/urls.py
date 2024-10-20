from django.urls import path
from .views import *

urlpatterns = [
    path('weather/', getWeather, name='weather'),
    path('search_city_weather/', getWeather, name='get_city_weather'),
    path('save_thresholds/', setThresholds, name='save_thresholds'),
    path('check_alerts/', getAlerts, name='check_alerts'),
    path('get_cities/', get_cities, name='get_cities'),
    path('get_summary/<str:city>/', getSummary, name='get_summary'),
    path('get_trends/<str:city>/<str:period>/', getTrends, name='get_trends')
]