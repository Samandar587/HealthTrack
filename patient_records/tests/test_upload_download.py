from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.test import APIClient
from patient_records.models import MedicalFile, Patient
from patient_records.rest_api.serializers import MedicalFileSerializer

class MedicalFileViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # create a patient
        self.patient = Patient.objects.create(
            name='John Doe',
            dob='1980-01-01',
            gender='M',
            address='123 Main St'
        )

        # create a medical file
        self.medical_file = MedicalFile.objects.create(
            patient=self.patient,
            file=SimpleUploadedFile('test_file.txt', b'Test file content')
        )

    def test_download(self):
        response = self.client.get(f'/api/medical-files/{self.medical_file.id}/download/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('Content-Disposition'), f'attachment; filename="{self.medical_file.file.name}"')
        self.assertEqual(response.content, b'Test file content')

    def test_upload(self):
        file_data = SimpleUploadedFile('test_file.txt', b'New test file content')
        response = self.client.post(f'/api/medical-files/{self.medical_file.id}/upload/', {'file': file_data}, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, MedicalFileSerializer(self.medical_file).data)
        self.medical_file.refresh_from_db()
        self.assertEqual(self.medical_file.file.read(), b'New test file content')
