from datetime import datetime, timedelta
from .models import weekly_session_new, extra_session, sessions , Week
from django.db import transaction


# Sort sessions by type function
def sort_sessions_by_type(sessions):
    session_type_order = {"Cours": 0, "Td": 1, "Tp": 2}
    sorted_sessions = sorted(sessions, key=lambda session: session_type_order.get(session.type_session.nom, float('inf')))
    return sorted_sessions

# Function to set heure sup information
@transaction.atomic
def set_heure_sup(sorted_sessions, charge, MAX_CHARGE, Coef, unit):
    MAX_CHARGE = MAX_CHARGE * unit
    
    for session in sorted_sessions:
        if session.type_session.nom == "Cours" and charge < MAX_CHARGE:
            charge += Coef * unit
            session.is_heure_sup = False
            session.save()

    if charge < MAX_CHARGE:
        for session in sorted_sessions:
            charge += unit
            session.is_heure_sup = False
            session.save()
    
    for session in sorted_sessions:
        if charge > MAX_CHARGE:
            session.is_partially_heure_sup = True
            session.is_heure_sup = False
            session.partially_heure_sup(unit, charge - MAX_CHARGE)
            session.save()

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

# Function to get weeks with dates between two dates
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

# Main function to create sessions for weeks
def create_sessions_for_weeks(start_date, end_date, teacher_id):
    weeks_with_dates = dates_with_days_between(start_date, end_date)

    for week_index, week in enumerate(weeks_with_dates):
        week_sessions = []
        week_start_date = week[0][0]
        week_end_date = week[-1][0]
        week_month = datetime.strptime(week_start_date, '%Y-%m-%d').month
        week_number = week_index + 1

        for date, day in week:
            date_dt = datetime.strptime(date, '%Y-%m-%d')
            weekly_sessions = weekly_session_new.objects.filter(
                enseignant_id=teacher_id, selectedDay=day
            ).select_related('type_session')
            extra_sessions = extra_session.objects.filter(
                enseignant=teacher_id, date=date_dt
            ).select_related('type_session')

            for ws in weekly_sessions:
                session = sessions(
                    enseignant=ws.enseignant,
                    semestre=ws.semestre,
                    Departement=ws.Departement,
                    Promo=ws.Promo,
                    Section=ws.Section,
                    group=ws.group,
                    selectedDay=ws.selectedDay,
                    heure_debut=ws.heure_debut,
                    heure_fin=ws.heure_fin,
                    module=ws.module,
                    type_session=ws.type_session,
                    salle=ws.salle,
                    date=date_dt
                )
                week_sessions.append(session)

            for es in extra_sessions:
                session = sessions(
                    enseignant=es.enseignant,
                    semestre=es.semestre,
                    Departement=es.Departement,
                    Promo=es.Promo,
                    Section=es.Section,
                    group=es.group,
                    selectedDay=es.selectedDay,
                    heure_debut=es.heure_debut,
                    heure_fin=es.heure_fin,
                    module=es.module,
                    type_session=es.type_session,
                    salle=es.salle,
                    date=es.date
                )
                week_sessions.append(session)

        # Bulk create sessions
        sessions.objects.bulk_create(week_sessions)

        # Set heure sup for the week
        sorted_week_sessions = sort_sessions_by_type(week_sessions)
        set_heure_sup(sorted_week_sessions, charge=0, MAX_CHARGE=11, Coef=1.5, unit=1)

        # Create a Week instance and associate the sessions with it
        week_instance = Week.objects.create(
            week_number=week_number,
            month=week_month,
            start_date=week_start_date,
            end_date=week_end_date,
        )
        week_instance.sessions.set(week_sessions)
        week_instance.save()
        print(f"Created week: {week_instance}")

# input : start_date, end_date, teacher_id | output : charge_duration and sup_duration ( minutes )in this period for this specific teacher
 
def calculate_charge_and_sup(date_debut, date_fin, teacher_id):
    total_charge_minutes = 0
    total_sup_minutes = 0
    # Ensure date_debut and date_fin are datetime objects
    if isinstance(date_debut, str):
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()
    if isinstance(date_fin, str):
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()

    # Filter sessions within the given date range and for the specific teacher
    session_list = sessions.objects.filter(date__range=[date_debut, date_fin], enseignant=teacher_id)

    # Process each session
    for session in session_list:
        debut_time = datetime.strptime(session.heure_debut, '%H:%M').time()
        fin_time = datetime.strptime(session.heure_fin, '%H:%M').time()
        duration_minutes = (fin_time.hour * 60 + fin_time.minute) - (debut_time.hour * 60 + debut_time.minute)
        if session.is_heure_sup:
            total_sup_minutes += duration_minutes
        else:
            if session.is_partially_heure_sup :
                total_sup_minutes += session.duration_sup
                total_charge_minutes += session.duration_charge
            else:
                total_charge_minutes += duration_minutes

    return total_charge_minutes, total_sup_minutes



""" 
those are some sql queries to get a week sessions ( you have to make join cus its one to many relatioshiop)
##
SELECT COUNT(*) FROM testing_week_sessions WHERE week_id = 1; 
##
SELECT w.id AS week_id, s.id AS session_id, s.date, s.type_session_id FROM testing_week_sessions ws JOIN testing_week w ON w.id = ws.week_id JOIN testing_sessions s ON s.id = ws.sessions_id WHERE w.id = 1;
"""