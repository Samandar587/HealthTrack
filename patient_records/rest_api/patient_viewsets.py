from rest_framework import viewsets, status
from patient_records.models import Patient
from .serializers import PatientSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class =  PatientSerializer
    permission_classes = [IsAuthenticated]

    # Creates a new object and saves it into database
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            response = {
                "success":False,
                "error":str(e)
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        
        response = {
            "success": True,
            "data": serializer.data
        }

        return Response(response)
    
    # Retrieves a patient object from database by id
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except Exception as e:
            response = {
                "success":False,
                "message":str(e)
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(instance)
        
        response = {
            "success":True,
            "data":serializer.data
        }

        return Response(response)
    
    # Updates a patient object's details
    def update(self, request, *args, **kwargs):     
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
        except ValidationError as e:
            response = {
                "success":False,
                "message":str(e)
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "success":False,
                "message":str(e)
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        response = {
            "success":True,
            "data": serializer.data
        }
        return Response(response)

    # Deletes a patient object from databse by id
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()   
        except Exception as e:
            response = {
                "success":False,
                "message":str(e),
            }
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(instance)

        response = {
            "success":True,
            "message": "Object has been successfully deleted!"
        }

        return Response(response)
