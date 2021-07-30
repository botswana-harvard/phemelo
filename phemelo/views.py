from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import PatientReport
from .serializers import PatientReportSerializer


@api_view(['GET', 'POST'])
def patient_reports(request):
    if request.method == 'GET':
        reports = PatientReport.objects.all()
        serializer = PatientReportSerializer(reports, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PatientReportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
