from datetime import datetime, timedelta
from django.utils.translation import gettext as _

def get_days_in_interval(start_date, end_date):
    days = []
    current_date = start_date
    while current_date <= end_date:
        day_name = _(current_date.strftime('%A'))  # Get localized day name
        days.append(f"{day_name} {current_date.strftime('%d-%m')}")
        current_date += timedelta(days=1)
    return days

# Example usage
start_date = datetime(2023, 9, 24)
end_date = datetime(2024, 1, 31)
days_within_interval = get_days_in_interval(start_date, end_date)
print(days_within_interval)
