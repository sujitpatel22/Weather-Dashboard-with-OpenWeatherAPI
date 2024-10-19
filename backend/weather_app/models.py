# models.py

from django.db import models
from django.contrib.auth.models import User


class WeatherData(models.Model):
    main_condition = models.CharField(max_length=50, null=True)
    temperature = models.FloatField(null=True)
    feels_like = models.FloatField(null=True)
    humidity = models.IntegerField(null=True)
    wind_speed = models.FloatField(null=True)
    last_update = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.city} - {self.main_condition} at {self.last_update}"


class DailyWeatherSummary(models.Model):
    date = models.DateField(null=True)
    avg_temp = models.FloatField(null=True)
    max_temp = models.FloatField(null=True)
    min_temp = models.FloatField(null=True)
    avg_humidity = models.FloatField(null=True)
    avg_wind_speed = models.FloatField(null=True)
    dominant_condition = models.CharField(max_length=50, null=True)


class City(models.Model):
    city = models.CharField(max_length=100)
    weather = models.ManyToManyField(WeatherData)
    daily_weather = models.ManyToManyField(DailyWeatherSummary)

    def __str__(self):
        return f"Summary for {self.city} on {self.date}"


class AggregationStatus(models.Model):
    last_aggregated_date = models.DateField(auto_now_add=True)


class WeatherAlertThreshold(models.Model):
    city = models.CharField(max_length=100)
    temp_threshold = models.FloatField(
        null=True, blank=True)  # Temperature threshold
    wind_speed_threshold = models.FloatField(
        null=True, blank=True)  # Wind speed threshold
    humidity_threshold = models.IntegerField(
        null=True, blank=True)  # Humidity threshold
    consecutive_updates = models.IntegerField(
        default=2)  # Default to 2 consecutive updates

    def __str__(self):
        return f"Thresholds for {self.city}"
