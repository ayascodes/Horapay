from datetime import datetime, timedelta
from .models import weekly_session_new, extra_session

# Mapping from English day names to French day names
day_mapping = {
    'Monday': 'Lundi',
    'Tuesday': 'Mardi',
    'Wednesday': 'Mercredi',
    'Thursday': 'Jeudi',
    'Friday': 'Vendredi',
    'Saturday': 'Samedi',
    'Sunday': 'Dimanche'
}

def dates_with_days_between(start_date, end_date):
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = datetime.strptime(end_date, '%Y-%m-%d')
    weeks_list = []

    current_week = []
    week_month = start_dt.month
    current_dt = start_dt

    while current_dt <= end_dt:
        if current_dt.weekday() == 6 and current_dt != start_dt:
            if current_week:
                weeks_list.append(current_week)
            current_week = []
            week_month = current_dt.month

        if current_dt.month != week_month:
            if current_week:
                weeks_list.append(current_week)
            current_week = []
            week_month = current_dt.month

        day_name = day_mapping[current_dt.strftime('%A')]
        current_week.append((current_dt.strftime('%Y-%m-%d'), day_name))
        current_dt += timedelta(days=1)

    if current_week:
        weeks_list.append(current_week)

    return weeks_list

def create_sessions_for_weeks(start_date, end_date, teacher_id):
    from .models import sessions
    weeks_with_dates = dates_with_days_between(start_date, end_date)

    for week in weeks_with_dates:
        for date, day in week:
            date_dt = datetime.strptime(date, '%Y-%m-%d')
            print(f"Processing date: {date}, day: {day}")

            # Filter weekly sessions for the teacher and the specific day
            weekly_sessions = weekly_session_new.objects.filter(enseignant_id=teacher_id, selectedDay=day)
            print(f"Found {weekly_sessions.count()} weekly sessions for {day} (teacher_id: {teacher_id})")

            for ws in weekly_sessions:
                sessions.objects.create(
                    enseignant=ws.enseignant,
                    semestre=ws.semestre,
                    Departement=ws.Departement,
                    Promo=ws.Promo,
                    Section=ws.Section,
                    group=ws.group,
                    selectedDay=day,
                    heure_debut=ws.heure_debut,
                    heure_fin=ws.heure_fin,
                    module=ws.module,
                    type_session=ws.type_session,
                    salle=ws.salle,
                    date=date_dt
                )
                print(f"Created session from weekly session: {ws.id} on {date}")

            # Filter extra sessions for the teacher and the specific date
            extra_sessions = extra_session.objects.filter(enseignant_id=teacher_id, date=date_dt)
            print(f"Found {extra_sessions.count()} extra sessions for {date} (teacher_id: {teacher_id})")

            for es in extra_sessions:
                sessions.objects.create(
                    enseignant=es.enseignant,
                    semestre=es.semestre,
                    Departement=es.Departement,
                    Promo=es.Promo,
                    Section=es.Section,
                    group=es.group,
                    selectedDay=day,
                    heure_debut=es.heure_debut,
                    heure_fin=es.heure_fin,
                    module=es.module,
                    type_session=es.type_session,
                    salle=es.salle,
                    date=es.date
                )
                print(f"Created session from extra session: {es.id} on {date}")
