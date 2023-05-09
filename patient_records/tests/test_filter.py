from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from datetime import date, timedelta
from patient_records.models import Patient
from patient_records.rest_api.serializers import PatientSerializer
from patient_records.rest_api.filter import PatientFilter, PatientList

class PatientListTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.patient1 = Patient.objects.create(
            name='John Doe',
            dob=date.today() - timedelta(days=30),
            gender='M',
            address='123 Main St'
        )
        self.patient2 = Patient.objects.create(
            name='Jane Smith',
            dob=date.today() - timedelta(days=60),
            gender='F',
            address='456 Elm St'
        )

    def test_filter_by_name(self):
        url = reverse('patient-list')
        response = self.client.get(url, {'name': 'john'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Doe')

    def test_filter_by_dob(self):
        url = reverse('patient-list')
        response = self.client.get(url, {'dob': date.today() - timedelta(days=30)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Doe')

    def test_filter_by_gender(self):
        url = reverse('patient-list')
        response = self.client.get(url, {'gender': 'F'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Jane Smith')

    def test_filter_by_address(self):
        url = reverse('patient-list')
        response = self.client.get(url, {'address': '123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'John Doe')

    def test_create_patient(self):
        url = reverse('patient-list')
        data = {
            'name': 'Bob Johnson',
            'dob': date.today() - timedelta(days=45),
            'gender': 'M',
            'address': '789 Oak St'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 3)
        self.assertEqual(Patient.objects.last().name, 'Bob Johnson')

class PatientFilterTestCase(TestCase):
    def setUp(self):
        self.patient1 = Patient.objects.create(
            name='John Doe',
            dob=date.today() - timedelta(days=30),
            gender='M',
            address='123 Main St'
        )
        self.patient2 = Patient.objects.create(
            name='Jane Smith',
            dob=date.today() - timedelta(days=60),
            gender='F',
            address='456 Elm St'
        )

    def test_filter_by_name(self):
        qs = Patient.objects.all()
        filtered_qs = PatientFilter({'name': 'john'}, queryset=qs).qs
        self.assertEqual(filtered_qs.count(), 1)
        self.assertEqual(filtered_qs.first(), self.patient1)

    def test_filter_by_dob(self):
        qs = Patient.objects.all()
        filtered_qs = PatientFilter({'dob': date.today() - timedelta(days=30)}, queryset=qs).qs
        self.assertEqual(filtered_qs.count(), 1)
        self.assertEqual(filtered_qs)
