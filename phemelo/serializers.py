from rest_framework import serializers

from .models import PatientReport


class PatientReportSerializer(serializers.ModelSerializer):

    scan_copy = serializers.FileField(max_length=None, allow_empty_file=False)

    class Meta:
        model = PatientReport
        fields = '__all__'
