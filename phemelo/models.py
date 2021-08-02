import os
from django.db import models


class PatientReport(models.Model):

    patient_id = models.CharField(
        max_length=50,
        unique=True)

    patient_name = models.CharField(max_length=50)

    examiner_notes = models.TextField()

    scan_datetime = models.DateTimeField()

    scan_location = models.CharField(max_length=50)

    scan_operator = models.CharField(max_length=50)

    scan_reason = models.CharField(max_length=50)

    scan_copy = models.FileField(upload_to='scans/%Y/%m/%d/')

    def filename(self):
        return os.path.basename(self.file.name)

    class Meta:
        app_label = 'phemelo'
