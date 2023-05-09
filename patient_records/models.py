from django.db import models

class Patient(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    medical_history = models.JSONField(default=dict)


class MedicalFile(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    file = models.FileField(upload_to='medical_files/')