from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
# Create your models here.
class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    GRADE_CHOICES = [
        ('assistant master a','Assistant Master A'),
        ('assistant master b','Assistant Master B'),
        ('lecturer a','Lecturer A'),
        ('lecturer b','Lecturer B'),
        ('teacher','Teacher'),
        ('professor','Professor'),
    ]
    PHONE_NUMBER_REGEX = r'^0[567][0-9]{8}$'
    phone_number_validator = RegexValidator(
        regex=PHONE_NUMBER_REGEX,
        message='Phone number must be 10 digits and start with 07, 05, or 06.'
    )

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    is_admin = models.BooleanField(default=False)
    #fields below are for teacher only
    is_recruited = models.BooleanField(default=False)
    grade = models.CharField(max_length=50, null = True ,blank=True , choices=GRADE_CHOICES) # needs more costumisaton
    date_of_birth = models.DateField(null=True)
    is_responsable = models.BooleanField(default=False)
    RIP = models.CharField(max_length=10 ,null = True,unique=True) # IS UNNIIIIIIIIIQUE
    phone_number = models.CharField(max_length=10,  null = True ,blank=True,validators=[phone_number_validator])


    def __str__(self):
        if self.is_admin:
            return f"{self.first_name} {self.last_name}, admin"
        elif self.grade:
            return f"{self.first_name} {self.last_name}, {self.get_grade_display()}"
        else:
            return f"{self.first_name} {self.last_name}"

""" post ;
{
  "username": "lamia_gasmi",
  "password": "azertyuiop",
  "gender": "male",
  "is_admin": false,
  "is_recruited": false,
  "grade": null,
  "date_of_birth": "1990-01-01",
  "is_responsable": false,
  "RIP": null,
  "phone_number": "0555555555"
} """

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
    pass
    
"""  creating instence : 
exams_instance = Exams.objects.create(datedebut='2024-01-01', datefin='2024-01-05', description='Final exam') 

 """

""" how to link the reason with the session ? : foreinkey between reason table and session table
# Assuming you have already created an Exams instance

# Now, create a Session instance linked to the Exams instance
session_instance = Session.objects.create(date='2024-01-01', reason=exams_instance) 
 """