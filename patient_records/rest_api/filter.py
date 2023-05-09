from django_filters import rest_framework as filters
from rest_framework import generics
from patient_records.models import Patient
from .serializers import PatientSerializer

class PatientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    dob = filters.DateFilter(field_name='dob')

    class Meta:
        model = Patient
        fields = ['name', 'dob', 'gender', 'address']

class PatientList(generics.ListCreateAPIView): 
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    filterset_class = PatientFilter

