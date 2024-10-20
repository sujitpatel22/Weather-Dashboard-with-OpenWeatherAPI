from .models import City
from django.shortcuts import get_object_or_404
from .models import WeatherAlertThreshold, WeatherData, City
from datetime import datetime, time
import json
import os
import requests
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views import View
from dotenv import load_dotenv
from .models import *
from django.db.models import Avg, Max, Min
from collections import Counter
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, timedelta, time
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# Load API_KEY from .env file through django.conf.settings
api_key = settings.API_KEY

@csrf_exempt
def getWeather(request):
    weather_data = []
    if request.method == 'POST':
        data = json.loads(request.body)
        cities = [data.get('city')]
    else:
        cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']

    for city in cities:
        url = f'https://api.openweathermap.org/data/2.5/weather?q={city},India&APPID={api_key}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather = data['weather'][0]
            main = data['main']
            wind = data['wind']
            weather_data.append({
                'name': data['name'],
                'mainCondition': weather['main'],
                # Convert Kelvin to Celsius
                'temperature': main['temp'] - 273.15,
                # Convert Kelvin to Celsius
                'feelsLike': main['feels_like'] - 273.15,
                'humidity': main['humidity'],
                'windSpeed': wind['speed'],
                'lastUpdate': data['dt'],
            })
            weather = WeatherData(
                main_condition=weather['main'],
                temperature=main['temp'] - 273.15,
                feels_like=main['feels_like'] - 273.15,
                humidity=main['humidity'],
                wind_speed=wind['speed'],
                last_update=datetime.utcfromtimestamp(data['dt']),
                created_at=datetime.now()
            )
            weather.save()
            city_object, _ = City.objects.get_or_create(city=city)
            city_object.weather.add(weather)
            city_object.save()
        else:
            weather_data.append(
                {'name': city, 'error': 'Data not available'})

    return JsonResponse(weather_data, safe=False)


def calculate_daily_aggregates():
    # Get today's and yesterday's date
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    # Get all distinct cities from WeatherData
    cities = City.objects.all()
    for city in cities:
        # Get weather data for the city from yesterday
        daily_data = city.weather.filter(last_update__date=yesterday)
        if not daily_data.exists():
            return JsonResponse({'Error': 'No data found for selected period!'})
        # Calculate aggregates for temperature, humidity, and wind speed
        avg_temp = daily_data.aggregate(Avg('temperature'))[
            'temperature__avg']
        max_temp = daily_data.aggregate(Max('temperature'))[
            'temperature__max']
        min_temp = daily_data.aggregate(Min('temperature'))[
            'temperature__min']
        avg_humidity = daily_data.aggregate(
            Avg('humidity'))['humidity__avg']
        avg_wind_speed = daily_data.aggregate(Avg('wind_speed'))[
            'wind_speed__avg']
        # Determine the dominant weather condition
        conditions = [entry.main_condition for entry in daily_data]
        dominant_condition = Counter(conditions).most_common(1)[0][0]
        # Update or create DailyWeatherSummary
        weather_summary, created = DailyWeatherSummary.objects.update_or_create(
            date=yesterday,
            defaults={
                'avg_temp': avg_temp,
                'max_temp': max_temp,
                'min_temp': min_temp,
                'avg_humidity': avg_humidity,
                'avg_wind_speed': avg_wind_speed,
                'dominant_condition': dominant_condition,
            }
        )
        # If it's a new summary, add it to the city's daily weather
        if created:
            city.daily_weather.add(weather_summary)


def get_cities(request):
    cities = City.objects.all().values('id', 'city')
    return JsonResponse(list(cities), safe=False)


def getSummary(request, city):
    # Get the current date in the correct timezone
    today = timezone.localtime().date()  # Use localtime to ensure correct timezone

    try:
        # Fetch the city object
        city = City.objects.get(city=city)
    except City.DoesNotExist:
        return JsonResponse({'error': 'City not found'}, status=404)

    # Start of the current day (in the same timezone)
    start_of_day = timezone.make_aware(datetime.combine(
        today, time(0, 0, 0)), timezone.get_current_timezone())
    current_time = timezone.localtime()  # Ensure current time is localized

    # Fetch weather data using `created_at` for the current day (from 00:00 AM to now)
    weather_data = city.weather.filter(
        created_at__gte=start_of_day, created_at__lte=current_time)

    if not weather_data.exists():
        return JsonResponse({'error': 'No weather data found for the city today'})

    # Calculate aggregates
    avg_temp = round(weather_data.aggregate(
        Avg('temperature'))['temperature__avg'], 2)
    max_temp = round(weather_data.aggregate(
        Max('temperature'))['temperature__max'], 2)
    min_temp = round(weather_data.aggregate(
        Min('temperature'))['temperature__min'], 2)
    avg_humidity = round(weather_data.aggregate(
        Avg('humidity'))['humidity__avg'], 2)
    avg_wind_speed = round(weather_data.aggregate(
        Avg('wind_speed'))['wind_speed__avg'], 2)

    # Prepare the response data
    data = {
        'city': city.city,
        'avg_temp': avg_temp,
        'max_temp': max_temp,
        'min_temp': min_temp,
        'avg_humidity': avg_humidity,
        'avg_wind_speed': avg_wind_speed,
        'last_update': current_time,
    }

    return JsonResponse(data)


# class ThresholdBreachAlert(View):
@csrf_exempt
def setThresholds(request):
    if request.method == "POST":
        data = json.loads(request.body)
        city = data.get('city')
        temp_threshold = data.get('temp_threshold')
        wind_speed_threshold = data.get('wind_speed_threshold')
        humidity_threshold = data.get('humidity_threshold')
        consecutive_updates = data.get('consecutive_updates', 2)
        # Create or update the alert threshold for this city
        threshold, created = WeatherAlertThreshold.objects.update_or_create(
            city=city,
            defaults={
                'temp_threshold': temp_threshold,
                'wind_speed_threshold': wind_speed_threshold,
                'humidity_threshold': humidity_threshold,
                'consecutive_updates': consecutive_updates
            }
        )
        return JsonResponse({'message': 'Thresholds saved successfully.'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)


def getAlerts(request):
    thresholds = WeatherAlertThreshold.objects.all()
    alerts = []

    for threshold in thresholds:
        try:
            # Get the city object from the threshold city name
            city_obj = City.objects.get(city=threshold.city)
        except City.DoesNotExist:
            continue  # Skip this threshold if city is not found

        # Fetch the last two weather updates for this city from its related WeatherData
        recent_updates = city_obj.weather.order_by(
            '-last_update')[:threshold.consecutive_updates]

        if recent_updates.count() == threshold.consecutive_updates:
            # Extract weather data
            temps = [update.temperature for update in recent_updates]
            wind_speeds = [update.wind_speed for update in recent_updates]
            humidities = [update.humidity for update in recent_updates]

            # Check if temperature exceeds threshold
            if threshold.temp_threshold is not None and all(temp > threshold.temp_threshold for temp in temps):
                alerts.append(
                    f"Temperature in {threshold.city} exceeded {threshold.temp_threshold}°C for the last {threshold.consecutive_updates} updates."
                )

            # Check if wind speed exceeds threshold
            if threshold.wind_speed_threshold is not None and all(wind > threshold.wind_speed_threshold for wind in wind_speeds):
                alerts.append(
                    f"Wind speed in {threshold.city} exceeded {threshold.wind_speed_threshold} m/s for the last {threshold.consecutive_updates} updates."
                )

            # Check if humidity exceeds threshold
            if threshold.humidity_threshold is not None and all(hum > threshold.humidity_threshold for hum in humidities):
                alerts.append(
                    f"Humidity in {threshold.city} exceeded {threshold.humidity_threshold}% for the last {threshold.consecutive_updates} updates."
                )

    return JsonResponse({"alerts": alerts})


def getTrends(request, city, period):
    city = get_object_or_404(City, city=city)

    # Time frame filter based on user selection
    if period == '1_week':
        days = 7
    elif period == '15_days':
        days = 15
    elif period == '30_days':
        days = 30
    elif period == '2_months':
        days = 60  # Approximate for 2 months
    elif period == '6_months':
        days = 180  # Approximate for 6 months
    else:
        return JsonResponse({'error': 'Invalid time frame'}, status=400)

    # Fetching the daily weather data for the specified time frame
    daily_weather_data = city.daily_weather.all().order_by('-date')[:days]
    weather_trends = {
        'dates': [],
        'avg_temp': [],
        'max_temp': [],
        'min_temp': [],
        'avg_humidity': [],
        'avg_wind_speed': [],
    }

    convert_date_format = lambda date_str: datetime.strptime(date_str, '%Y-%m-%d').strftime('%d-%m-%y')

    for entry in daily_weather_data:
        weather_trends['dates'].append(convert_date_format(entry.date.isoformat()))
        weather_trends['avg_temp'].append(entry.avg_temp)
        weather_trends['max_temp'].append(entry.max_temp)
        weather_trends['min_temp'].append(entry.min_temp)
        weather_trends['avg_humidity'].append(entry.avg_humidity)
        weather_trends['avg_wind_speed'].append(entry.avg_wind_speed)

    return JsonResponse(weather_trends)

