from django.urls import path
from .views import *

urlpatterns = [
    path('weather/', WeatherDataView.as_view(), name='weather_data'),
    path('save_thresholds/', ThresholdBreachAlert.as_view(), name='save_thresholds'),
    path('check_alerts/', ThresholdBreachAlert.as_view(), name='save_thresholds'),
    path('weather_visuals/<str:period>/', WeatherVisuals.as_view(), name='weather_visuals')
]