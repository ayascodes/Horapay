from rest_framework import serializers
from .models import *

from rest_framework import serializers
from .models import *

        
class CustomUserSerialize(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

#Reason subclasses 
#this is a common date validator :
class DateRangeValidationMixin:
    def validate(self, data):
        if data['datedebut'] > data['datefin']:
            raise serializers.ValidationError("La date de début doit être antérieure à la date de fin.")
        return data
    
class ExamsSerializer(DateRangeValidationMixin,serializers.ModelSerializer):
    class Meta:
        model = Exams
        fields = '__all__'

class VacationSerializer(DateRangeValidationMixin,serializers.ModelSerializer):
    class Meta:
        model = Vacation
        fields = '__all__'

class StageSerializer(DateRangeValidationMixin,serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = '__all__'

class JourFeriesSerializer(DateRangeValidationMixin,serializers.ModelSerializer):
    class Meta:
        model = JourFeries
        fields = '__all__'

class AbsenceSerializer(DateRangeValidationMixin,serializers.ModelSerializer):
    class Meta:
        model = Absence
        fields = '__all__'

#report
        
class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'