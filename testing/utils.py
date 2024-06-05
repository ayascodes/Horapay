from datetime import datetime, timedelta
from .models import *
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
    print("Welcome inside set_heure_sup")
    index = 0

    while index < len(sorted_sessions) and sorted_sessions[index].type_session.nom == "Cours" and charge < MAX_CHARGE:
        print("Processing Cours session")
        charge += Coef * unit
        sorted_sessions[index].is_heure_sup = False
        # Do not set duration_charge and duration_sup here
        print(f"Index: {index}, Charge: {charge}, Session ID: {sorted_sessions[index].id}")
        sorted_sessions[index].save()
        index += 1

    print(f"Exited first loop with Charge: {charge}, MAX_CHARGE: {MAX_CHARGE}")

    if charge == MAX_CHARGE:
        print("Charge completed, remaining sessions will be heure sup")
    elif charge < MAX_CHARGE:
        print("Charge less than MAX_CHARGE, processing additional sessions")
        while index < len(sorted_sessions) and charge < MAX_CHARGE:
            print(f"Processing session type: {sorted_sessions[index].type_session.nom} with id {sorted_sessions[index].id}")
            charge += unit
            print("charge inside inf ",charge)
            sorted_sessions[index].is_heure_sup = False
            # Do not set duration_charge and duration_sup here
            sorted_sessions[index].save()
            index += 1

        if charge == MAX_CHARGE:
            print(f"end of while 2 :Charge completed: {charge}/{MAX_CHARGE}")
        elif charge > MAX_CHARGE :
            print(f"end of while 2 : Charge exceeded : {charge}/{MAX_CHARGE}")
            print(f"FROM EXCEEDED : Index: {index}, Charge: {charge}")
            sorted_sessions[index - 1].is_partially_heure_sup = True
            sorted_sessions[index - 1].is_heure_sup = False
            diff_charge = charge - MAX_CHARGE
            sorted_sessions[index - 1].partially_heure_sup(unit, diff_charge)
            print(f"Is partially heure sup: {sorted_sessions[index].is_partially_heure_sup}")
            print(f"Is heure sup: {sorted_sessions[index].is_heure_sup}")
            sorted_sessions[index].save()

    else:
        print(f"Charge exceeded: {charge}/{MAX_CHARGE}")
        print(f"FROM EXCEEDED: Index: {index}, Charge: {charge}")
        sorted_sessions[index - 1].is_partially_heure_sup = True
        sorted_sessions[index - 1].is_heure_sup = False
        diff_charge = charge - MAX_CHARGE
        sorted_sessions[index - 1].partially_heure_sup(unit, diff_charge)
        print(f"Is partially heure sup: {sorted_sessions[index].is_partially_heure_sup}")
        print(f"Is heure sup: {sorted_sessions[index].is_heure_sup}")
        sorted_sessions[index].save()

    return sorted_sessions
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
#-------------------------------
from django.db.models import Q

def is_date_within_reason_periods(date):
    overlapping_periods = (
        Q(datedebut__lte=date, datefin__gte=date)
    )

    # Check each model separately except for Absence
    exams_exist = Exams.objects.filter(overlapping_periods).exists()
    vacation_exist = Vacation.objects.filter(overlapping_periods).exists()
    stage_exist = Stage.objects.filter(overlapping_periods).exists()
    jour_feries_exist = JourFeries.objects.filter(overlapping_periods).exists()

    return exams_exist or vacation_exist or stage_exist or jour_feries_exist

#Helper Function:

#The is_date_within_reason_periods function checks if the given date falls within any period defined by Exams, Vacation, Stage, JourFeries, or Absence for the specific teacher.
#The overlapping_periods query ensures that the date lies within the start and end dates of any reason.
#The exclude clause excludes periods that are not related to the specific teacher for the Absence model.
#-------------------------------------
# Main function to create sessions for weeks
@transaction.atomic
@transaction.atomic
def create_sessions_for_weeks(start_date, end_date, teacher_id):
    weeks_with_dates = dates_with_days_between(start_date, end_date)

    for week_index, week in enumerate(weeks_with_dates):
        week_sessions = []
        week_start_date = week[0][0]
        week_end_date = week[-1][0]
        week_month = datetime.strptime(week_start_date, '%Y-%m-%d').month
        week_number = week_index + 1
        week_duration_sup = 0  # Initialize week's total Duration_sup

        for date, day in week:
            date_dt = datetime.strptime(date, '%Y-%m-%d')
            if is_date_within_reason_periods(date_dt):
                continue  # Skip creating this session

            weekly_sessions = weekly_session_new.objects.filter(
                enseignant_id=teacher_id, selectedDay=day
            ).select_related('type_session')
            extra_sessions = extra_session.objects.filter(
                enseignant=teacher_id, date=date_dt
            ).select_related('type_session')

            for ws in weekly_sessions:
                if not sessions.objects.filter(
                    enseignant=ws.enseignant,
                    date=date_dt,
                    heure_debut=ws.heure_debut,
                    heure_fin=ws.heure_fin,
                    type_session=ws.type_session
                ).exists():
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
                    session.save()
                    week_sessions.append(session)

            for es in extra_sessions:
                if not sessions.objects.filter(
                    enseignant=es.enseignant,
                    date=es.date,
                    heure_debut=es.heure_debut,
                    heure_fin=es.heure_fin,
                    type_session=es.type_session
                ).exists():
                    session = sessions(
                        enseignant=es.enseignant,
                        semestre=es.semestre,
                        Departement=es.Departement,
                        Promo=es.Promo,
                        Section=es.Section,
                        group=es.group,
                        selectedDay=day_mapping[es.date.strftime('%A')],
                        heure_debut=es.heure_debut,
                        heure_fin=es.heure_fin,
                        module=es.module,
                        type_session=es.type_session,
                        salle=es.salle,
                        date=es.date
                    )
                    session.save()
                    week_sessions.append(session)

        # Sort the sessions by type
        sorted_sessions = sort_sessions_by_type(week_sessions)

        # Set heure sup information
        charge = 0  # This should be the initial charge, which you may need to calculate or pass as a parameter
        MAX_CHARGE = 5.25  # Set this to your maximum charge value
        Coef = 1.5  # Set this to your coefficient value
        unit = 1  # Set this to the unit value in minutes

        sorted_sessions = set_heure_sup(sorted_sessions, charge, MAX_CHARGE, Coef, unit)

        # Calculate total Duration_sup for the week
        for session in sorted_sessions:
            if session.is_heure_sup:
                # Calculate session duration in hours
                session_duration = (datetime.strptime(session.heure_fin, '%H:%M') - datetime.strptime(session.heure_debut, '%H:%M')).seconds / 3600
                week_duration_sup += session_duration
            elif session.is_partially_heure_sup:
                week_duration_sup += session.duration_sup / 60  # Convert minutes to hours

        # Create or update the Week object
        week_obj, created = Week.objects.get_or_create(
            week_number=week_number,
            month=week_month,
            defaults={
                'start_date': week_start_date,
                'end_date': week_end_date,
                'Duration_sup': round(week_duration_sup, 2)  # Round to 2 decimal places
            }
        )

        if not created:
            week_obj.Duration_sup = round(week_duration_sup, 2)
            week_obj.save()

        # Add the sessions to the Week object
        week_obj.sessions.set(sorted_sessions)
        week_obj.save()

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
            if session.is_partially_heure_sup:
                total_sup_minutes += session.duration_sup
                total_charge_minutes += session.duration_charge
            else:
                total_charge_minutes += duration_minutes

    return total_charge_minutes, total_sup_minutes
