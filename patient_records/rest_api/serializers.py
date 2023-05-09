from rest_framework import serializers
from patient_records.models import Patient, MedicalFile

class MedicationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    dosage = serializers.CharField(max_length=100)
    frequency = serializers.CharField(max_length=100)

class MedicalHistorySerializer(serializers.Serializer):
    conditions = serializers.ListField(child=serializers.CharField(max_length=100))
    allergies = serializers.ListField(child=serializers.CharField(max_length=100))
    medications = MedicationSerializer(many=True)

class PatientSerializer(serializers.ModelSerializer):
    medical_history = MedicalHistorySerializer()

    class Meta:
        model = Patient
        fields = '__all__'
        read_only_fields = ['id']


class MedicalFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalFile
        fields = '__all__'

