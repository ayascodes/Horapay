from datetime import datetime

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from .validators import validate_academic_year_format
from django.core.exceptions import ValidationError


# Create your models here.

class UserType(models.Model):
    TYPE_CHOICES = [
        ('Enseignant', 'Enseignant'),
        ('Administrateur', 'Administrateur')
    ]
    Type = models.CharField(max_length=20, choices=TYPE_CHOICES)


class Grade(models.Model):
    nom = models.CharField(max_length=20)
    prix_heure = models.IntegerField()
    couleur = models.CharField(max_length=50,default=None)

class MaxHeureSup(models.Model):
    max_charge=models.PositiveIntegerField()
    max_supp = models.PositiveIntegerField()


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
    ]
    GRADE_CHOICES = [
        ('assistant master a', 'assistant master a'),
        ('assistant master a', 'assistant master b'),
        ('lecteur a', 'lecteur a'),
        ('lecteur b', 'lecteur b'),
        ('enseignant', 'enseignant'),
        ('professeur', 'professeur'),
    ]
    PAYMENT_CHOICES = [
        ('rib', 'RIB'),
        ('ccp clé', 'Ccp Clé'),
    ]
    PHONE_NUMBER_REGEX = r'^0[567][0-9]{8}$'
    phone_number_validator = RegexValidator(
        regex=PHONE_NUMBER_REGEX,
        message='Phone number must be 10 digits and start with 07, 05, or 06.'
    )
    nom = models.CharField(max_length=20, null=False, default=None)
    prenom = models.CharField(max_length=20, null=False, default=None)
    email = models.EmailField(unique=True, null=False)
    # mot_de_passe=models.CharField(max_length=8,null=False,default=None)
    UserType = models.CharField(max_length=20, null=True)
    sexe = models.CharField(max_length=10, choices=GENDER_CHOICES, null=False, default='Homme')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    # fields below are for teacher only
    education = models.CharField(max_length=20, null=True, blank=True)
    # grade = models.CharField(max_length=50, null=True, blank=True, choices=GRADE_CHOICES)  # needs more costumisaton
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, default=1)
    # date de naissance
    DAYS_CHOICES = [(i, f"{i} days") for i in range(1, 31)]

    jour = models.IntegerField(choices=DAYS_CHOICES, null=False, default=1986)
    MONTHS_CHOICES = [
        ('01', 'Janvier'),
        ('02', 'Février'),
        ('03', 'Mars'),
        ('04', 'Avril'),
        ('05', 'Mai'),
        ('06', 'Juin'),
        ('07', 'Juillet'),
        ('08', 'Août'),
        ('09', 'Septembre'),
        ('10', 'Octobre'),
        ('11', 'Novembre'),
        ('12', 'Décembre'),
    ]
    mois = models.CharField(max_length=10, choices=MONTHS_CHOICES, null=False, default=1)
    current_year = datetime.now().year
    YEARS_CHOICES = [(i, str(i)) for i in range(1923, current_year + 1)]
    annee = models.IntegerField(choices=YEARS_CHOICES, null=False, default=1)
    responsable = models.BooleanField(default=False)
    # payemnt_info = models.CharField(max_length=20 ,null = True,unique=True , choices=PAYMENT_CHOICES) # IS UNNIIIIIIIIIQUE
    RIB = models.CharField(max_length=10, null=True, unique=True)
    ccp = models.CharField(max_length=10, null=True, unique=True)
    cle = models.CharField(max_length=2, null=True, unique=True)
    numero_telephone = models.CharField(max_length=10, null=True, blank=True, validators=[phone_number_validator])
    reset_password_token = models.CharField(max_length=100, blank=True, null=True)
    charge_actuel = models.IntegerField(null=True)
    heure_sup_actuel = models.IntegerField(null=True)
    Photo_profil = models.ImageField(upload_to='photo_profil/',blank=True,null=True)
    full_name = models.CharField(max_length=50,default=None)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    first_name = None
    last_name = None

    def clean(self):

        # Get the selected month and year
        month = self.mois
        year = self.annee
        # Check if February and if it's a leap year
        if month == 2:
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                # Leap year, February has 29 days
                if self.day > 29:
                    raise ValidationError('Février a 29 jours en années bissextiles.')
            else:
                # Non-leap year, February has 28 days
                if self.day > 28:
                    raise ValidationError('Février a 28 jours en années non bissextiles.')
        elif month in [4, 6, 9, 11] and self.day > 30:
            # Months with 30 days
            raise ValidationError('Ce mois a 30 jours.')

    def __str__(self):
        if self.is_admin:
            return f"{self.nom} {self.prenom}, admin"
        elif self.grade:
            return f"{self.nom} {self.prenom}, {self.get_grade_display()}"
        else:
            return f"{self.nom} {self.prenom}"




# error_consultation / rapport
class Report(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               limit_choices_to={'is_admin': False})  # Only teachers
    description = models.TextField()
    date_time = models.DateTimeField(auto_now_add=True)
    status_choices = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')

    def __str__(self):
        return f"Report by {self.sender} - {self.date_time}"


# reason :
class Reason(models.Model):
    datedebut = models.DateField()
    datefin = models.DateField()
    description = models.CharField(max_length=100)

    class Meta:
        abstract = True  # Make this an abstract base class ( template or blueprint for the subclasses (Exams, Vacation, Stage, JourFeries, Absence).)


# Abstract models are only used as base classes for other models and are not stored in the database themselves.

# we can add other fields

class Exams(Reason):
    pass


class Vacation(Reason):
    pass


class Stage(Reason):
    pass


class JourFeries(Reason):
    pass


class Absence(Reason):
    enseignant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    is_justified = models.BooleanField(default=False)


"""  creating instence : 
exams_instance = Exams.objects.create(datedebut='2024-01-01', datefin='2024-01-05', description='Final exam') 

 """

""" how to link the reason with the session ? : foreinkey between reason table and session table
# Assuming you have already created an Exams instance

# Now, create a Session instance linked to the Exams instance
session_instance = Session.objects.create(date='2024-01-01', reason=exams_instance) 
 """


class Semestre(models.Model):
    annee_academique = models.CharField(max_length=9, validators=[validate_academic_year_format])
    numero_de_semestre = models.IntegerField(choices=[(1, '1'), (2, '2')], default=1)
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return f"Semestre {self.numero_de_semestre} - {self.annee_academique}"


class Departement(models.Model):
    CYCLE_PREPARATOIRE = 'Cycle préparatoire'
    CYCLE_SUPERIEUR = 'Cycle supérieur'

    CYCLE_CHOICES = [
        (CYCLE_PREPARATOIRE, 'Cycle préparatoire'),
        (CYCLE_SUPERIEUR, 'Cycle supérieur')
    ]
    nom = models.CharField(max_length=20, choices=CYCLE_CHOICES, default=CYCLE_PREPARATOIRE)

    def __str__(self):
        return f"{self.nom}"


class Specialite(models.Model):
    nom = models.CharField(max_length=20, default='null')

    def __str__(self):
        return self.nom


class Salle(models.Model):
    TYPE_CHOICES = [
        ('AMPHI', 'Amphitheatre'),
        ('TP', 'Salle Tp'),
        ('TD', 'Salle Td')
    ]
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, null=False)
    SalleType = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Amphitheatre')
    SalleName = models.CharField(max_length=50)
    SalleCapacity = models.PositiveIntegerField()

    def str(self):
        return f" {self.SalleType} {self.SalleName} - {self.departement}"


class Promo(models.Model):
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, null=False, default=1)

    nom = models.CharField(max_length=20, null=True)
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE, null=True)

    def __str__(self):
        if self.specialite is None:
            return f"{self.nom} - {self.departement}"
        else:
            return f"{self.nom} - {self.departement}-{self.specialite}"


class Section(models.Model):
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE)
    nom = models.CharField(max_length=1)

    def __str__(self):
        return f" Section {self.nom} - {self.promo}"


class Group(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    numero_du_group = models.IntegerField()

    def __str__(self):
        return f"Group {self.nombre_du_group}-{self.section}-{self.semestre}"


class Module(models.Model):
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE)
    nom = models.CharField(max_length=20)
    credit = models.IntegerField()
    coefficient = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"

class Type_seance(models.Model):
    nom = models.CharField(max_length=15)
    def __str__(self):
        return f"{self.nom}"
class Weekly_session(models.Model):
    Day_CHOICES = [
        ('Samedi', 'Samedi'),
        ('Dimanche', 'Dimanche'),
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi')
    ]
    TYPE_SESSION_CHOICES = [
        ('Cours', 'Cours'),
        ('TD', 'TD'),
        ('TP', 'TP')
    ]
    POUR_CHOICES = [
        ('Que pour une semaine', 'Que pour une semaine'),
        ('Pour le semestre', 'Pour le semestre')
    ]
    enseignant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, default=1)
    Departement = models.ForeignKey(Departement, on_delete=models.CASCADE, default=1)
    Promo = models.ForeignKey(Promo, on_delete=models.CASCADE, default=1)
    Section = models.ForeignKey(Section, on_delete=models.CASCADE, default=1)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None)
    selectedOption = models.CharField(max_length=20, choices=POUR_CHOICES, default='Que pour une semaine')
    #date = models.DateField(null=True)
    selectedDay = models.CharField(max_length=10, choices=Day_CHOICES, default='Dimanche', null=True, blank=True)
    heure_supp = models.BooleanField(default=False)
    heure_debut = models.IntegerField(null=True,blank=True)
    heure_fin = models.IntegerField(null=True,blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, default=None)
    type_session=models.ForeignKey(Type_seance,on_delete=models.CASCADE,default=None)
    #type_session = models.CharField(max_length=10, choices=TYPE_SESSION_CHOICES, default='Cours')
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"weekly {self.type_session} {self.module} {self.enseignant}"
    
class anysession(models.Model):
    Day_CHOICES = [
        ('Samedi', 'Samedi'),
        ('Dimanche', 'Dimanche'),
        ('Lundi', 'Lundi'),
        ('Mardi', 'Mardi'),
        ('Mercredi', 'Mercredi'),
        ('Jeudi', 'Jeudi')
    ]
    
    enseignant = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE, default=1)
    Departement = models.ForeignKey(Departement, on_delete=models.CASCADE, default=1)
    Promo = models.ForeignKey(Promo, on_delete=models.CASCADE, default=1)
    Section = models.ForeignKey(Section, on_delete=models.CASCADE, default=1)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None)
    heure_debut = models.CharField(max_length=5, null=True, blank=True)
    heure_fin = models.CharField(max_length=5, null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, default=None)
    type_session = models.ForeignKey(Type_seance, on_delete=models.CASCADE, default=None)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE, default=None)

    class Meta:
        abstract = True

class weekly_session_new(anysession):
    selectedDay = models.CharField(max_length=10, choices=anysession.Day_CHOICES, default='Dimanche', null=True, blank=True)

class extra_session(anysession):
    date = models.DateField(null=True)

from datetime import time

class sessions(anysession):
    selectedDay = models.CharField(max_length=10, choices=anysession.Day_CHOICES, default='Dimanche', null=True, blank=True)
    date = models.DateField(null=True)
    is_heure_sup = models.BooleanField(default=True)
    is_partially_heure_sup = models.BooleanField(default=False)
    duration_charge = models.IntegerField(null=True, blank=True)  # Duration in minutes
    duration_sup = models.IntegerField(null=True, blank=True)  # Duration in minutes

    def __str__(self):
        return f"session {self.type_session.nom} {self.selectedDay} {self.date}"

    def partially_heure_sup(self, unit, diff_charge):
        unit_minutes = 60 / unit
        diff_charge_minute = diff_charge * unit_minutes

        # Parse heure_debut and heure_fin strings to extract hours and minutes
        heure_debut_hours, heure_debut_minutes = map(int, self.heure_debut.split(':'))
        heure_fin_hours, heure_fin_minutes = map(int, self.heure_fin.split(':'))

        # Calculate the duration in minutes
        debut_time = datetime.strptime(self.heure_debut, '%H:%M').time()
        fin_time = datetime.strptime(self.heure_fin, '%H:%M').time()
        duration_minutes = (fin_time.hour * 60 + fin_time.minute) - (debut_time.hour * 60 + debut_time.minute)

        # Calculate the part charge in minutes
        part_charge_minutes = diff_charge_minute

        # Calculate the part of the session that is heure sup in minutes
        part_heure_sup_minutes = duration_minutes - part_charge_minutes

        # Assign values to the new fields
        self.duration_charge = part_charge_minutes
        self.duration_sup = part_heure_sup_minutes
        self.save()
class Etablissement(models.Model):
    nom_fr = models.CharField(max_length=100)
    nom_ar = models.CharField(max_length=100)
    ministere_fr = models.CharField(max_length=100)
    ministere_ar = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='logos/', blank=True, null=True)


