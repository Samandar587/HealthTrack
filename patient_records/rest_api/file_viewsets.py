from .serializers import MedicalFileSerializer
from rest_framework import viewsets
from patient_records.models import MedicalFile
from rest_framework.decorators import action

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
        with open(file_path, 'rb') as f:
            file_data = f.read()
        response = Response(file_data, content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="%s"' % medical_file.file.name
        return response

    
    @action(detail=True, methods=['POST'])
    def upload(self, request, pk=None):
        medical_file = self.get_object()
        medical_file.file = request.FILES['file']
        medical_file.save()
        serializer = MedicalFileSerializer(medical_file)
        return Response(serializer.data, status=status.HTTP_200_OK)
