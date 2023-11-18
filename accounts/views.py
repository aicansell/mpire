from django.shortcuts import get_object_or_404

from rest_framework.exceptions import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_tracking.mixins import LoggingMixin

from authentication.models import User
from accounts.serializers import UserSerializer

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
        }
        
        serializer = UserSerializer(instance, data=request_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response = {
            'status': "Sucess",
            "message": "Data Updated Successfully",
        }
        
        return Response(response, status=status.HTTP_200_OK)
