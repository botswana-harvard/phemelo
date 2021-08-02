from redcap import Project, RedcapError
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, viewsets

from .models import PatientReport
from .serializers import PatientReportSerializer


class PatientReportViewSet(viewsets.ModelViewSet):

    serializer_class = PatientReportSerializer
    queryset = PatientReport.objects.all()


@api_view(['GET', 'POST'])
def patient_reports(request):
    if request.method == 'GET':
        reports = PatientReport.objects.all()
        serializer = PatientReportSerializer(reports, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PatientReportSerializer(data=request.data)
        if 'file' in request.FILES and serializer.is_valid():
            handle_uploaded_file(request.FILES['file'])
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def redcap_trigger(request):
    if request.method == 'GET':
        pass

    elif request.method == 'POST':
        token = 'BC5A95A9BEF533A16E0B02939D9AE902'
        data_dict = request.POST.dict()
        form_name = data_dict.get('instrument')
        if form_name == 'baseline_assessment':
            project = Project('https://redcap-dev.bhp.org.bw/api/', token)

            # query the reports for a scan copy for the given pid
            record_data = project.export_records(
                records=[data_dict.get('record'), ], fields=['scr_omang', ])

            patient_id = record_data[0].get('scr_omang') if record_data else None

            scan_copies = get_patient_scan(identifier=patient_id)
            # if exists import file(s) to the redcap
            # multiple files will have to be merged first
            file_path = scan_copies.file.name
            existing_fname = 'to_upload.pdf'
            fobj = scan_copies.file


def redcap_file_import(project, data_dict={}, file_obj=None, filename=''):
    field = 'ba_ibe_findings'
    # In the REDCap UI, the link to download the file will be named the fname you pass as the ``fname`` parameter
    try:
        response = project.import_file(
            record=data_dict.get('record'), field=field, fname=filename, fobj=file_obj)
    except RedcapError:
        # Your import didn't work
        pass
    finally:
        file_obj.close()


def get_participant_id(project):
    pass


def get_patient_scan(identifier=None):
    """ Query patient records for given patient id, and return copies of scan
        results findings.
        @param identifier: patient id (omang)
        @return: result findings scan (.pdf) files
    """
    try:
        report = PatientReport.objects.get(patient_id=identifier)
    except PatientReport.DoesNotExist:
        return None
    else:
        return report.scan_copy


def merge_copies(scan_copies=[]):
    """ Merge .pdf copies (if multiple) of the findings for REDCap import.
        REDCap only accepts single file for file field.
        @param scan_copies: copies of the scans (if multiple)
        @return: merged copy of scans (.pdf) file
    """
    pass


def handle_uploaded_file(f):
    with open(f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
