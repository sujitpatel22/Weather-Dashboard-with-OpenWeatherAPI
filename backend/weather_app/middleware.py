from datetime import datetime, time
from django.utils.timezone import now
from .models import AggregationStatus
from .views import calculate_daily_aggregates

class DailyAggregateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Before processing the request, trigger the aggregation check
        self.check_and_aggregate()

        # Continue with the response processing
        response = self.get_response(request)
        return response

    def check_and_aggregate(self):
        now_time = now()
        today = now_time.date()

        # Define the exact time for the daily aggregation (midnight)
        midnight = time(0, 0, 0)  # 12:00 AM midnight

        # Ensure that the aggregation only runs after midnight and within a short period after 12 AM (e.g., 12:00 AM - 12:05 AM)
        if now_time.time() >= midnight and now_time.time() < time(0, 5):  # 5-minute window after 12:00 AM
            status, created = AggregationStatus.objects.get_or_create(id=1)  # Assuming a single row
            
            if status.last_aggregated_date < today:
                # Run the daily aggregation task
                calculate_daily_aggregates()
                # Update the last aggregated date
                status.last_aggregated_date = today
                status.save()
