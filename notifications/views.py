from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_tracking.mixins import LoggingMixin

from notifications.models import Notification, Message
from notifications.serializers import NotificationSerializer, NotificationCreateSerializer, MessageSerializer

class MessageViewSet(LoggingMixin, ViewSet):
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(Message, pk=pk)
    
    @staticmethod
    def get_queryset():
        return Message.objects.all()
    
    def list(self, request):
        data = self.get_queryset()
        serializer = MessageSerializer(data, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        instance = self.get_object(pk)
        serializer = MessageSerializer(instance)
        return Response(serializer.data)
    
    def create(self, request):
        request_data = {
            'message': request.data.get('message'),
        }
        
        serializer = MessageSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response = {
            'status': 'success',
            'message': "Message created successfully",
        }
        
        return Response(response, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk):
        instance = self.get_object(pk)
        
        instance.message = request.data.get('message')
        instance.save()
        
        response = {
            'status': 'success',
            'message': "Message updated successfully",
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        
        response = {
            'status': 'success',
            'message': "Message deleted successfully",
        }
        
        return Response(response, status=status.HTTP_200_OK)

    
class NotificationViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(Notification, pk=pk)
    
    @staticmethod
    def get_queryset():
        return Notification.objects.all()
    
    def list(self, request):
        data = self.get_queryset()
        data = data.filter(user = request.user)
        serializer = NotificationSerializer(data, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        instance = self.get_object(pk)
        serializer = NotificationSerializer(instance)
        return Response(serializer.data)
    
    def create(self, request):
        request_data = {
            'user': request.data.get('user'),
            'message': request.data.get('message'),
            'title': request.data.get('title'),
        }
        
        try:
            for id in request_data.get('user'):
                request_data['user'] = id
                serializer = NotificationCreateSerializer(data=request_data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                
                response = {
                        'status': 'success',
                        'message': "Notification created successfully",
                }
        
                return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                'status': 'error',
                'message': str(e),
            }
            
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        

    def update(self, request, pk):
        instance = self.get_object(pk)
        
        instance.mark_read = True
        instance.save()
        
        response = {
            'status': 'success',
            'message': "Notification updated successfully",
        }
        
        return Response(response, status=status.HTTP_200_OK)
    
    def destroy(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        
        response = {
            'status': 'success',
            'message': "Notification deleted successfully",
        }
        
        return Response(response, status=status.HTTP_200_OK)
