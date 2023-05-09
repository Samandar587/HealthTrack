from rest_framework import routers
from .patient_viewsets import PatientViewSet
from .file_viewsets import MedicalFileViewSet
from django.urls import path, include
from .filter import PatientList

router = routers.DefaultRouter()
router.register(r'patient', PatientViewSet)
router.register(r'medical_files', MedicalFileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/medical_files/<int:pk>/download/', MedicalFileViewSet.as_view({'get': 'download'}), name='medicalfile-download'),
    path('api/filtered_patients/', PatientList.as_view())
]