from datetime import timedelta
from django.core.exceptions import ValidationError


def validate_academic_year_format(value):
    if not value or len(value) != 9 or not value[:4].isdigit() or value[4] != '/' or not value[5:].isdigit():
        raise ValidationError('Veuillez saisir l\'année académique dans le format AAAA/AAAA')


def get_weeks_between(date_debut, date_fin):

    weeks = []
    current_date = date_debut - timedelta(days=date_debut.weekday())  # Align to previous Sunday

    while current_date <= date_fin:
        if (current_date < date_debut):
            week_start = date_debut
        else :

            
            week_start = current_date

        week_end = current_date + timedelta(days=6)  # Always point to Saturday

        # Adjust week_end if it falls after date_fin
        if week_end > date_fin:
            week_end = date_fin

        weeks.append((week_start, week_end))

        current_date += timedelta(days=7)

    return weeks


def get_date_for_weeklysession(weekstart, day_name):
    
    if day_name == "Dimanche":
        day1to7 = 1
    elif day_name == "Lundi":
        day1to7 = 2
    elif day_name == "Mardi":
        day1to7 = 3
    elif day_name == "Mercredi":
        day1to7 = 4
    elif day_name == "Jeudi":
        day1to7 = 5
    elif day_name == "Samedi":
        day1to7 = 7

    return weekstart + day1to7 - 1