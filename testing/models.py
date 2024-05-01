from datetime import datetime

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from .validators import validate_academic_year_format
from django.core.exceptions import  ValidationError

# Create your models here.

class UserType(models.Model):
    TYPE_CHOICES=[
        ('Enseignant','Enseignant'),
        ('Administrateur','Administrateur')
    ]
    Type=models.CharField(max_length=20,choices=TYPE_CHOICES)
class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
    ]
    GRADE_CHOICES = [
    ('assistant master a', 'Assistant Master A'),
    ('assistant master b', 'Assistant Master B'),
    ('lecteur a', 'Lecteur A'),
    ('lecteur b', 'Lecteur B'),
    ('enseignant', 'Enseignant'),
    ('professeur', 'Professeur'),
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
    email = models.EmailField(unique=True)
    UserType = models.ForeignKey(UserType, on_delete=models.CASCADE,default=1)
    sexe = models.CharField(max_length=10, choices=GENDER_CHOICES,null=False,default='Homme')
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    #fields below are for teacher only
    education= models.CharField(default=False)
    grade = models.CharField(max_length=50, null = True ,blank=True , choices=GRADE_CHOICES) # needs more costumisaton
    #date de naissance
    DAYS_CHOICES = [(i, f"{i} days") for i in range(1, 31)]

    jour = models.IntegerField(choices=DAYS_CHOICES,null=False,default=1986)
    MONTHS_CHOICES = [
        ('Janvier', 'Janvier'),
        ('Février', 'Février'),
        ('Mars', 'Mars'),
        ('Avril', 'Avril'),
        ('Mai', 'Mai'),
        ('Juin', 'Juin'),
        ('Juillet', 'Juillet'),
        ('Août', 'Août'),
        ('Septembre', 'Septembre'),
        ('Octobre', 'Octobre'),
        ('Novembre', 'Novembre'),
        ('Décembre', 'Décembre'),
    ]
    mois = models.CharField(max_length=10,choices=MONTHS_CHOICES,null=False,default=1)
    current_year = datetime.now().year
    YEARS_CHOICES = [(i,str(i)) for i in range(1923,current_year+1)]
    annee = models.IntegerField(choices=YEARS_CHOICES,null=False,default=1)
    responsable = models.BooleanField(default=False)
    #payemnt_info = models.CharField(max_length=20 ,null = True,unique=True , choices=PAYMENT_CHOICES) # IS UNNIIIIIIIIIQUE
    RIB = models.CharField(max_length=10, null=True, unique=True)
    ccp = models.CharField(max_length=10,null=True, unique=True)
    cle = models.CharField(max_length=2,null=True,unique=True)
    numero_telephone = models.CharField(max_length=10,  null = True ,blank=True,validators=[phone_number_validator])
    reset_password_token = models.CharField(max_length=100, blank=True, null=True)
    charge_actuel=models.IntegerField(null=True)
    heure_sup_actuel=models.IntegerField(null=True)
    username = None
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def clean(self):

       #Get the selected month and year
       month = self.month
       year = self.year
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
            return f"{self.first_name} {self.last_name}, admin"
        elif self.grade:
            return f"{self.first_name} {self.last_name}, {self.get_grade_display()}"
        else:
            return f"{self.first_name} {self.last_name}"

#error_consultation / rapport
class Report(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_admin': False})  # Only teachers
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
#Abstract models are only used as base classes for other models and are not stored in the database themselves.

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
    numero_de_semestre = models.IntegerField(choices=[(1,'1'),(2,'2')], default=1)
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
    nom = models.CharField(max_length=20,choices=CYCLE_CHOICES, default=CYCLE_PREPARATOIRE)

    def __str__(self):
        return f"{self.nom}"

class Specialite(models.Model):

    nom = models.CharField(max_length=20,default='null')
    def __str__(self):
         return self.nom

class Salle(models.Model):
        TYPE_CHOICES = [
            ('AMPHI', 'Amphitheatre'),
            ('TP', 'Salle Tp'),
            ('TD', 'Salle Td')
        ]
        departement = models.ForeignKey(Departement, on_delete=models.CASCADE, null=False)
        type_salle = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Amphitheatre')
        nom_salle = models.CharField(max_length=50)
        capacite = models.PositiveIntegerField()

        def __str__(self):
            return f" {self.type_salle} {self.nom_salle} - {self.departement}"
class Promo(models.Model):
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE,null=False,default=1)

    nom = models.CharField(max_length=20,null=True)
    specialite = models.ForeignKey(Specialite,on_delete=models.CASCADE,null=True)
    def __str__(self):
        if self.specialite is None:
            return f"{self.nom} - {self.departement}"
        else:
            return f"{self.nom} - {self.departement}-{self.specialite}"
class Section(models.Model):
    promo=models.ForeignKey(Promo, on_delete=models.CASCADE)
    nom=models.CharField(max_length=1)
    def __str__(self):
       return f" Section {self.nom} - {self.promo}"

class Group(models.Model):
    semestre=models.ForeignKey(Semestre,on_delete=models.CASCADE)
    section = models.ForeignKey(Section,on_delete=models.CASCADE)
    nombre_du_group = models.IntegerField()

    def __str__(self):
        return f"Group {self.nombre_du_group}-{self.section}-{self.semestre}"

class Module(models.Model):
    semestre = models.ForeignKey(Semestre, on_delete=models.CASCADE)
    promo = models.ForeignKey(Promo, on_delete=models.CASCADE)
    nom = models.CharField(max_length=20)
    credit = models.IntegerField()
    coefficient=models.IntegerField()

    def __str__(self):
        return f"{self.nom}"
class Weekly_session(models.Model):
    Day_CHOICES = [
        ('1', 'Dimanche'),
        ('2', 'Lundi'),
        ('3', 'Mardi'), ('4', 'Mercredi'),
        ('5', 'Jeudi')
    ]
    TYPE_SESSION_CHOICES = [
        ('1', 'Cours'),
        ('2', 'TD'),
        ('3', 'TP')
    ]
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    salle = models.ForeignKey(Salle, on_delete=models.CASCADE)
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    jour = models.CharField(max_length=10, choices=Day_CHOICES, default='Dimanche')
    heure_debut = models.IntegerField()
    heure_fin = models.IntegerField()
    type_session = models.CharField(max_length=10, choices=TYPE_SESSION_CHOICES, default='Cours')

    def __str__(self):
        return f"weekly {self.session_type} {self.module} {self.teacher}"




