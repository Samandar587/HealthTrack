from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from patient_records.models import Patient
from patient_records.rest_api.serializers import PatientSerializer


class PatientViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.patient_data = {
            'name': 'Test Patient',
            'age': 30,
            'email': 'testpatient@example.com',
            'phone_number': '1234567890'
        }
        self.patient = Patient.objects.create(**self.patient_data)
        self.url = reverse('patient-list')
        self.detail_url = reverse('patient-detail', kwargs={'pk': self.patient.pk})

    def test_create_patient(self):
        response = self.client.post(self.url, self.patient_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Patient.objects.count(), 2)
        self.assertEqual(Patient.objects.last().name, 'Test Patient')

    def test_create_invalid_patient(self):
        invalid_data = {
            'name': 'Test Patient',
            'age': 'Invalid',
            'email': 'testpatient@example.com',
            'phone_number': '1234567890'
        }
        response = self.client.post(self.url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['success'], False)

    def test_retrieve_patient(self):
        response = self.client.get(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['data']['name'], 'Test Patient')

    def test_update_patient(self):
        updated_data = {
            'name': 'Updated Patient',
            'age': 35,
            'email': 'updatedpatient@example.com',
            'phone_number': '9876543210'
        }
        response = self.client.put(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['data']['name'], 'Updated Patient')
        self.assertEqual(response.data['data']['age'], 35)

    def test_partial_update_patient(self):
        updated_data = {
            'age': 35,
            'phone_number': '9876543210'
        }
        response = self.client.patch(self.detail_url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['success'], True)
        self.assertEqual(response.data['data']['age'], 35)
        self.assertEqual(response.data['data']['phone_number'], '9876543210')

    def test_delete_patient(self):
        response = self.client.delete(self.detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Patient.objects.count(), 0)



