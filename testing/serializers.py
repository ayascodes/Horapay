
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import *



class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'
class CustomUserSerialize(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=8,min_length=6,write_only=True
    )
    grade_nom = serializers.CharField(source='grade.nom', read_only=True)
    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        nom = validated_data.get('nom', instance.nom)
        prenom = validated_data.get('prenom', instance.prenom)
        instance.full_name = f"{nom} {prenom}"
        instance.save()
        return instance



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

class SemestreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semestre
        fields = '__all__'

class DepartementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departement
        fields = '__all__'

class SpecialiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialite
        fields = '__all__'

class SalleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Salle
        fields ='__all__'

class PromoSerializer(serializers.ModelSerializer):
    #departement_name = serializers.CharField(source='departement', write_only=True)
    #specialite_name = serializers.CharField(source='specialite', write_only=True)
    class Meta:
        model = Promo
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = '__all__'
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'

class Type_seanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type_seance
        fields = '__all__'
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = CustomUser
        fields = ['token']

class Weekly_sessionserializer(serializers.ModelSerializer):
    class Meta:
        model = Weekly_session
        fields = '__all__'

# this is for algorithm : 
class SessionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = sessions    
        fields = '__all__'

class WeeklySessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = weekly_session_new
        fields = '__all__'

class ExtraSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = extra_session
        fields = '__all__'

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()





class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[self.username_field] = serializers.EmailField()

    def validate(self,attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['usertype']=self.user.UserType
        return data

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'



class EtablissementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etablissement
        fields = '__all__'

class MaxHeureSupSerializer(serializers.ModelSerializer):
    class Meta:
        model=MaxHeureSup
        fields = '__all__'



# note : i forgot the reason table the father of absence, need to be fixed to the actual models

