from datetime import datetime, timedelta
from .models import weekly_session_new, extra_session, sessions


def sort_sessions_by_type(sessions):
    # Define the order of session types
    session_type_order = {"Cours": 0, "Td": 1, "Tp": 2}
    # Define a custom sorting key function
    def sorting_key(session):
        return session_type_order.get(session.type_session.nom, float('inf'))
    print("inside the sort function")
    for session in sessions:
        print(f"Session: {session}, Type: {session.type_session.nom}")
    # Sort the sessions based on their type using the custom sorting key
    sorted_sessions = sorted(sessions, key=sorting_key)
    return sorted_sessions

def set_heure_sup(sorted_sessions, charge, MAX_CHARGE, Coef, unit):
    MAX_CHARGE = MAX_CHARGE * unit
    index = 0
    print("ani barra ")
    print(len(sorted_sessions))
    print("inside set_heure_sup function")
    for session in sorted_sessions:
            print(f"Session: {session}, Type: {session.type_session.nom}")
    
    while index < len(sorted_sessions) and sorted_sessions[index].type_session.nom == "Cours" and charge < MAX_CHARGE:
        print("ani dkhalt ")
        print("while conditions : ")
        print(index < len(sorted_sessions))
        print(sorted_sessions[index].type_session.nom == "Cours")
        print(charge < MAX_CHARGE)
        charge += Coef * unit
        print("charge pour   ",sorted_sessions[index].type_session.nom,":", charge)
        sorted_sessions[index].is_heure_sup = False
        sorted_sessions[index].save()
        #if (index + 1) < len(sorted_sessions) and sorted_sessions[index + 1].type_session.nom == "Cours" and charge < MAX_CHARGE: index += 1
        index += 1
        print("index", index)
    index -= 1
    print("ani khrejt with   charge : ",charge,"et max charge : ",MAX_CHARGE,"index",index)
    if charge == MAX_CHARGE:
        print("charge completed")
        print("charge : " , charge , " | maxcharge : ",MAX_CHARGE)
    elif charge < MAX_CHARGE:
        print("charge < maxcharge")
        print("charge : " , charge , " | maxcharge : ",MAX_CHARGE)
        while index < len(sorted_sessions) and charge < MAX_CHARGE:
            charge += unit
            sorted_sessions[index].is_heure_sup = False
            sorted_sessions[index].save()
            index += 1
            print(index)
        print("end of while 2 : charge < maxcharge")
        print("charge : " , charge , " | maxcharge : ",MAX_CHARGE)
        if charge == MAX_CHARGE:
            print("charge completed after while 2 ")
        elif charge > MAX_CHARGE :
            sorted_sessions[index].is_partially_heure_sup = True
            sorted_sessions[index].is_heure_sup = False
            sorted_sessions[index].partially_heure_sup(unit, charge - MAX_CHARGE)
            sorted_sessions[index].save()
    else:
        print("charge > maxcharge")
        print("charge : " , charge , " | maxcharge : ",MAX_CHARGE)
        sorted_sessions[index].is_partially_heure_sup = True
        sorted_sessions[index].is_heure_sup = False
        sorted_sessions[index].partially_heure_sup(unit, charge - MAX_CHARGE)
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

def process_week(week):
    print(f"Processing week with {len(week)} days")
    for date, day in week:
        print(f"Date: {date}, Day: {day}")


def create_sessions_for_weeks(start_date, end_date, teacher_id):
    weeks_with_dates = dates_with_days_between(start_date, end_date)
    print("from weeks with dates : ",weeks_with_dates)
    for week in weeks_with_dates:
        process_week(week)  # Placeholder function for additional processing

        week_sessions = []  # Move inside the loop to create sessions for each week

        for date, day in week:
            date_dt = datetime.strptime(date, '%Y-%m-%d')
            print(f"Processing date: {date}, day: {day}")

            weekly_sessions = weekly_session_new.objects.filter(enseignant_id=teacher_id, selectedDay=day)
            print(f"Found {weekly_sessions.count()} weekly sessions for {day} (teacher_id: {teacher_id})")
            for ws in weekly_sessions:
                session = sessions.objects.create(
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
                week_sessions.append(session)
                print(f"Created session from weekly session: {ws.id} on {date}")

            extra_sessions = extra_session.objects.filter(enseignant=teacher_id, date=date_dt)
            print(f"Found {extra_sessions.count()} extra sessions for {date} (teacher_id: {teacher_id})")

            for es in extra_sessions:
                session = sessions.objects.create(
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
                week_sessions.append(session)
                print(f"Created session from extra session: {es.id} on {date}")
            print("inside weekly_sessions : " , week_sessions)

        # Set heure sup for the week
        print("am the week_sessions : ",week_sessions)
        print("Before sorting:")
        for session in week_sessions:
            print(f"Session: {session}, Type: {session.type_session}")
        sorted_week_sessions = sort_sessions_by_type(week_sessions)
        print("After sorting:")
        for session in sorted_week_sessions:
            print(f"Session: {session}, Type: {session.type_session}")
        print("am the sorted list : ",sorted_week_sessions)
        updated_sessions = set_heure_sup(sorted_week_sessions, charge=0, MAX_CHARGE=11, Coef=1.5, unit=1)


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
