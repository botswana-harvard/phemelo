from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from rest_framework import routers

from .views import patient_reports, redcap_trigger, PatientReportViewSet


router = routers.DefaultRouter()
router.register(r'patientreports', PatientReportViewSet)

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/reports/', patient_reports),
    path('api/v1/redcap_trigger_export/', redcap_trigger)]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
