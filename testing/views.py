from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated

# Users CRUD
class UsersList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerialize

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerialize

# CRUD for exams
class ExamsList(generics.ListCreateAPIView):
    queryset = Exams.objects.all()
    serializer_class = ExamsSerializer

class ExamsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exams.objects.all()
    serializer_class = ExamsSerializer

# CRUD for vacation
class VacationList(generics.ListCreateAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer

class VacationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer

# CRUD for stage
class StageList(generics.ListCreateAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer

class StageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer

# CRUD for absence
class AbsenceList(generics.ListCreateAPIView):
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer

class AbsenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer

# CRUD for jourferies
class JourFeriesList(generics.ListCreateAPIView):
    queryset = JourFeries.objects.all()
    serializer_class = JourFeriesSerializer

class JourFeriesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JourFeries.objects.all()
    serializer_class = JourFeriesSerializer

# CRUD for report
class ReportList(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ReportDetail(generics.RetrieveUpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

@api_view(['GET'])
def report_status(request, id):
    try:
        report = Report.objects.get(pk=id)
    except Report.DoesNotExist:
        return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        data = {'status': report.status}
        return Response(data)