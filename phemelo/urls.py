from django.urls import include, path
from rest_framework import routers

from .views import patient_reports


urlpatterns = [
    path('api/v1/reports/', patient_reports)]
