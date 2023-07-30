from .serializers import MedicalFileSerializer
from rest_framework import viewsets, status
from patient_records.models import MedicalFile, Patient
from rest_framework.decorators import action
from rest_framework.response import Response
import mimetypes
from django.http import FileResponse
import os


class MedicalFileViewSet(viewsets.ModelViewSet):
    queryset = MedicalFile.objects.all()
    serializer_class = MedicalFileSerializer

    def perform_create(self, serializer):
        patient_id = self.request.data.get('patient_id')
        patient = Patient.objects.get(id=patient_id)
        serializer.save(patient=patient)

    @action(detail=True, methods=['GET'])
    def download(self, request, pk=None):
        medical_file = self.get_object()
        file_path = medical_file.file.path
        content_type, encoding = mimetypes.guess_type(file_path)

        try:
            with open(file_path, 'rb') as file:
                if not content_type:
                    print("inside if content-type")
                    content_type = 'application/octet-stream'

                filename = os.path.basename(file_path)
                file_contents = file.read()  # Read the file contents into a variable

            response = Response(file_contents, content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename="{filename}"'

            return response

        except FileNotFoundError:
            return Response({"error": status.HTTP_404_NOT_FOUND})

    

        

    
    @action(detail=True, methods=['POST'])
    def upload(self, request, pk=None):
        # Retrieve the patient based on the provided pk (patient_id)
        patient = Patient.objects.get(id=pk)

        # Create a new MedicalFile object and assign the patient
        medical_file = MedicalFile(patient=patient)
        medical_file.file = request.FILES['file']
        medical_file.save()

        # Serialize the MedicalFile object and return the response
        serializer = MedicalFileSerializer(medical_file)
        return Response(serializer.data, status=status.HTTP_200_OK)
