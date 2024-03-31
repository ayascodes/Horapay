from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.decorators import api_view

# im using function-based views

@api_view(['GET','POST'])
def Users_list(request):

    if request.method == 'GET':
        users = CustomUser.objects.all()
        if users:
            serializer = CustomUserSerialize(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'POST':
        serializer = CustomUserSerialize(data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)



@api_view(['GET','PUT','DELETE'])
def Users_detail(request,id):

    try : 
        user = CustomUser.objects.get(pk=id)
    except  CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
       serializer = CustomUserSerialize(user)
       return Response(serializer.data)
    
    
    if request.method == 'PUT':
        serializer = CustomUserSerialize(user,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# reason subclasses
    #no need to set Crud for reason class cus its abstract base class we will not use it itself
#CRUD for exems 
@api_view(['GET', 'POST'])
def exams_list(request):
    if request.method == 'GET':
        exams = Exams.objects.all()
        serializer = ExamsSerializer(exams, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ExamsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def exams_detail(request, pk):
    try:
        exams = Exams.objects.get(pk=pk)
    except Exams.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ExamsSerializer(exams)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = ExamsSerializer(exams, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        exams.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
# CRUD for Vacation
@api_view(['GET', 'POST'])
def vacation_list(request):
    if request.method == 'GET':
        vacations = Vacation.objects.all()
        serializer = VacationSerializer(vacations, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VacationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def vacation_detail(request, pk):
    try:
        vacation = Vacation.objects.get(pk=pk)
    except Vacation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VacationSerializer(vacation)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = VacationSerializer(vacation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        vacation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# CRUD for Stage
@api_view(['GET', 'POST'])
def stage_list(request):
    if request.method == 'GET':
        stages = Stage.objects.all()
        serializer = StageSerializer(stages, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = StageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def stage_detail(request, pk):
    try:
        stage = Stage.objects.get(pk=pk)
    except Stage.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StageSerializer(stage)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = StageSerializer(stage, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        stage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
#CRUD for absence 
@api_view(['GET', 'POST'])
def absence_list(request):
    if request.method == 'GET':
        absences = Absence.objects.all()
        serializer = AbsenceSerializer(absences, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = AbsenceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def absence_detail(request, pk):
    try:
        absence = Absence.objects.get(pk=pk)
    except Absence.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = AbsenceSerializer(absence)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = AbsenceSerializer(absence, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        absence.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#CRUD for jourferies
@api_view(['GET', 'POST'])
def jour_feries_list(request):
    if request.method == 'GET':
        jours_feries = JourFeries.objects.all()
        serializer = JourFeriesSerializer(jours_feries, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = JourFeriesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def jour_feries_detail(request, pk):
    try:
        jour_feries = JourFeries.objects.get(pk=pk)
    except JourFeries.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JourFeriesSerializer(jour_feries)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = JourFeriesSerializer(jour_feries, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        jour_feries.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


 #report CRUD

@api_view(['GET', 'POST'])
def report_list(request):
        if request.method == 'GET':
            reports = Report.objects.all()
            serializer = ReportSerializer(reports, many=True)
            return Response(serializer.data)
        
        if request.method == 'POST':
            serializer = ReportSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

@api_view(['GET','PUT'])
def report_detail(request, id):
        try:
            report = Report.objects.get(pk=id)
        except Report.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = ReportSerializer(report)
            return Response(serializer.data)
        # admin approve or reject a report , sparated into 2 cases ; only status edited or status and description

        if request.method == 'PUT':
            new_status = request.data.get('status', None)
        if new_status is None:
            return Response({"error": "Status not provided"}, status=status.HTTP_400_BAD_REQUEST)

        if new_status not in ['APPROVED', 'REJECTED']:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update all fields if other data is provided in the request body
        serializer = ReportSerializer(report, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET'])
def report_status(request, id):
        try:
            report = Report.objects.get(pk=id)
        except Report.DoesNotExist:
            return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            data = {
            'status': report.status
            }
            return Response(data)

