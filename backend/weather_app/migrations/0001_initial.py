# Generated by Django 5.1.2 on 2024-10-19 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AggregationStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_aggregated_date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='DailyWeatherSummary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('avg_temperature', models.FloatField()),
                ('max_temperature', models.FloatField()),
                ('min_temperature', models.FloatField()),
                ('dominant_condition', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherAlertThreshold',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('temp_threshold', models.FloatField(blank=True, null=True)),
                ('wind_speed_threshold', models.FloatField(blank=True, null=True)),
                ('humidity_threshold', models.IntegerField(blank=True, null=True)),
                ('consecutive_updates', models.IntegerField(default=2)),
            ],
        ),
        migrations.CreateModel(
            name='WeatherData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=100)),
                ('main_condition', models.CharField(max_length=50)),
                ('temperature', models.FloatField()),
                ('feels_like', models.FloatField()),
                ('humidity', models.IntegerField()),
                ('wind_speed', models.FloatField()),
                ('last_update', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
