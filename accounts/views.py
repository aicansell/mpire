from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.exceptions import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from authentication.models import User, VendorModel
from accounts.serializers import UserSerializer, VendorSerializer

class UserViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get_object(pk):
        return get_object_or_404(User, pk=pk)
    
    @staticmethod
    def get_queryset():
        return User.objects.all()
    
    def retrieve(self, request, pk):
        instance = self.get_object(pk)
        serializer = UserSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk):
        instance = self.get_object(pk)
        
        request_data = {
            'email': request.data.get('email', instance.email),
            'first_name': request.data.get('first_name', instance.first_name),
            'last_name': request.data.get('last_name', instance.last_name),
            'state': request.data.get('state', instance.state),
            'first_time': request.data.get('first_time', instance.first_time),
        }
        
        serializer = UserSerializer(instance, data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response = {
            'status': "Sucess",
            "message": "Data Updated Successfully",
        }
        
        return Response(response, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        instance = self.get_object(pk)
        
        request_data = {
            'email': request.data.get('email', instance.email),
            'first_name': request.data.get('first_name', instance.first_name),
            'last_name': request.data.get('last_name', instance.last_name),
            'state': request.data.get('state', instance.state),
            'first_time': request.data.get('first_time', instance.first_time),
        }
        
        serializer = UserSerializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response = {
            'status': "Sucess",
            "message": "Data Updated Successfully",
        }
        
        return Response(response, status=status.HTTP_200_OK)

class VendorViewSet(ViewSet):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get_object(pk):
        return get_object_or_404(VendorModel, pk=pk)
    
    @staticmethod
    def get_queryset():
        return VendorModel.objects.all()
    
    def retrieve(self, request, pk):
        instance = self.get_object(pk)
        serializer = VendorSerializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        try:
            instance = VendorModel.objects.get(user=request.user)
            if instance:
                response = {
                    'status': "Failed",
                    "message": "Vendor Already Exists",
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        except VendorModel.DoesNotExist:
            request_data = {
                'user': request.user.id,
                'pancard': request.data.get('pancard'),
                'gst': request.data.get('gst'),
                'proof_of_registration': request.data.get('proof_of_registration'),
            }
            
            serializer = VendorSerializer(data=request_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            response = {
                'status': "Success",
                "message": "Data Created Successfully",
            }
            
            return Response(response, status=status.HTTP_200_OK)
        
    
    def update(self, request, pk):
        instance = self.get_object(pk)
        
        request_data = {
            'user': instance.user.id,
            'pancard': request.data.get('pancard', instance.pancard),
            'gst': request.data.get('gst', instance.gst),
            'proof_of_registration': request.data.get('proof_of_registration', instance.proof_of_registration),
            'approved': request.data.get('approved', instance.approved),
        }
        
        serializer = VendorSerializer(instance, data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response = {
            'status': "Success",
            "message": "Data Updated Successfully",
        }
        
        return Response(response, status=status.HTTP_200_OK)

    def partial_update(self, request, pk):
        instance = self.get_object(pk)
        
        request_data = {
            'pancard': request.data.get('pancard', instance.pancard),
            'gst': request.data.get('gst', instance.gst),
            'proof_of_registration': request.data.get('proof_of_registration', instance.proof_of_registration),
            'approved': request.data.get('approved', instance.approved),
        }
        
        serializer = VendorSerializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response = {
            'status': "Success",
            "message": "Data Updated Successfully",
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        
        response = {
            'status': "Success",
            "message": "Data Deleted Successfully",
        }
        
        return Response(response, status=status.HTTP_200_OK)

def HomeView(request):
    return HttpResponse("Welcome to the Home Page!")
