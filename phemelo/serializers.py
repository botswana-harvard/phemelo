from rest_framework import serializers

from .models import PatientReport


class PatientReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientReport
        fields = '__all__'
