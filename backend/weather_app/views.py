import json
import os
import requests
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.views import View
# from dotenv import load_dotenv
from .models import *
from django.db.models import Avg, Max, Min
from collections import Counter
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.mail import send_mail  # (optional)
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.utils.decorators import method_decorator

# Load environment variables from .env file
# load_dotenv()
# api_key = os.getenv('API_KEY')
cities = ['Delhi', 'Mumbai', 'Chennai', 'Bangalore', 'Kolkata', 'Hyderabad']
api_key = '3865500aead3e9aa7fa2f5c70689981a'


class WeatherDataView(View):
    def get(self, request):
        weather_data = []

        # get_weather_data()

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
                    last_update = datetime.utcfromtimestamp(data['dt']),
                    created_at = datetime.now()
                )
                weather.save()

                city_object, _ = City.objects.get_or_create(city=city)
                city_object.weather.add(weather)
                city_object.save()

            else:
                weather_data.append(
                    {'name': city, 'error': 'Data not available'})

        return JsonResponse(weather_data, safe=False)

class aggregatesView(View):
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
                city=city,  # Ensure City is related to DailyWeatherSummary
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

    def get(self, request):
        # Get today's date
        today = timezone.now().date()

        # Fetch the aggregation status
        aggregation_status = AggregationStatus.objects.first()

        # Check if aggregation needs to be performed
        if aggregation_status is None or aggregation_status.last_aggregated_date < today:
            # Perform aggregation if it hasn't been done today
            self.calculate_daily_aggregates()

            # Update or create aggregation status
            if aggregation_status:
                aggregation_status.last_aggregated_date = today
                aggregation_status.save()
            else:
                AggregationStatus.objects.create(last_aggregated_date=today)

        # Retrieve and return the latest weather data (summary for the last 7 days, for example)
        # Optional: Filter by city if provided in the request
        city_name = request.query_params.get('city', None)

        if city_name:
            # Retrieve weather summaries for the specified city
            city = City.objects.filter(city=city_name).first()
            if not city:
                return JsonResponse({'error': 'City not found'}, status=404)

            weather_summaries = city.daily_weather.filter(
                date__gte=today - timedelta(days=7))
        else:
            # Retrieve weather summaries for all cities for the last 7 days
            weather_summaries = DailyWeatherSummary.objects.filter(
                date__gte=today - timedelta(days=7))

        # Prepare the response data
        summary_data = []
        for summary in weather_summaries:
            summary_data.append({
                'city': summary.city.city,
                'date': summary.date,
                'avg_temp': summary.avg_temp,
                'max_temp': summary.max_temp,
                'min_temp': summary.min_temp,
                'avg_humidity': summary.avg_humidity,
                'avg_wind_speed': summary.avg_wind_speed,
                'dominant_condition': summary.dominant_condition,
            })
        return JsonResponse({'weather_summaries': summary_data}, status=200, safe=False)


class ThresholdBreachAlert(View):
    @requires_csrf_token
    def post(self, request):
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

    def get(self, request):
        thresholds = WeatherAlertThreshold.objects.all()
        alerts = []

        for threshold in thresholds:
            # Fetch the last two weather updates for this city
            recent_updates = WeatherData.objects.filter(city=threshold.city).order_by(
                '-timestamp')[:threshold.consecutive_updates]

            if recent_updates.count() == threshold.consecutive_updates:
                temps = [update.temp for update in recent_updates]
                wind_speeds = [update.wind_speed for update in recent_updates]
                humidities = [update.humidity for update in recent_updates]

                if threshold.temp_threshold and all(temp > threshold.temp_threshold for temp in temps):
                    alerts.append(
                        f"Temperature in {threshold.city} exceeded {threshold.temp_threshold}°C for the last {threshold.consecutive_updates} updates.")

                if threshold.wind_speed_threshold and all(wind > threshold.wind_speed_threshold for wind in wind_speeds):
                    alerts.append(
                        f"Wind speed in {threshold.city} exceeded {threshold.wind_speed_threshold} m/s for the last {threshold.consecutive_updates} updates.")

                if threshold.humidity_threshold and all(hum > threshold.humidity_threshold for hum in humidities):
                    alerts.append(
                        f"Humidity in {threshold.city} exceeded {threshold.humidity_threshold}% for the last {threshold.consecutive_updates} updates.")

        return JsonResponse({"alerts": alerts})


class WeatherVisuals(View):
    def get(self, request, period):
        if request.method == "POST":
            return JsonResponse({'error': 'Invalid Reqeust Method!'})

        today = timezone.now()
        if period == "1_week":
            start_date = today - timedelta(days=7)
        elif period == "10_days":
            start_date = today - timedelta(days=10)
        elif period == "1_month":
            start_date = today - timedelta(days=30)
        elif period == "2_months":
            start_date = today - timedelta(days=60)
        elif period == "6_months":
            start_date = today - timedelta(days=180)
        else:
            return JsonResponse({"error": "Invalid period"}, status=400)

        weather_data = DailyWeatherSummary.objects.filter(date__gte=start_date).values(
            'date').annotate(
            avg_temp=Avg('avg_temp'),
            max_temp=Max('max_temp'),
            min_temp=Min('min_temp'),
            avg_humidity=Avg('humidity'),
            avg_wind_speed=Avg('wind_speed')
        ).order_by('date')

        return JsonResponse(list(weather_data), safe=False)
