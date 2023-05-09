from django.urls import path, include
from patient_records.rest_api import urls

urlpatterns = [
    path('', include('rest_api.urls'))
]