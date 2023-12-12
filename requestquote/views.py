from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework_tracking.mixins import LoggingMixin

from requestquote.utils import send_quote_email
from requestquote.models import RequestQuote
from requestquote.serializers import RequestQuoteSerializer, RequestQuoteListSerializer

class RequestQuoteViewSet(LoggingMixin, ViewSet):
    permission_classes = [IsAuthenticated]
    
    @staticmethod
    def get_object(pk=None):
        return get_object_or_404(RequestQuote, pk=pk)
    
    @staticmethod
    def get_queryset():
        return RequestQuote.objects.all()
    
    def list(self, request):
        if request.user.user_type == 'customer':
            return Response({"status": "Unauthorized"}, status=status.HTTP_400_BAD_REQUEST)
        
        data = self.get_queryset()
        
        if request.user.user_type == 'vendor':
            data = data.filter(product__created_by = request.user)
        
        serializer = RequestQuoteListSerializer(data, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        instance = self.get_object(pk)
        serializer = RequestQuoteListSerializer(instance)
        return Response(serializer.data)
    
    def create(self, request):
        request_data = {
            'product': request.data.get('product'),
            'requestuser': request.user.id,
            'message': request.data.get('message'),
        }
        
        contact_me = request.data.get('contact_me')
        
        serializer = RequestQuoteSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        send_quote_email(serializer.instance, contact_me)
        
        response = {
            'status': 'success',
            'message': "Request Quote created successfully",
        }
        
        return Response(response)
    
    def update(self, request, pk):
        instance = self.get_object(pk)
        
        request_data = {
            'product': request.data.get('product', instance.product.id),
            'requestuser': instance.requestuser.id,
            'message': request.data.get('message', instance.message),
            'created_at': instance.created_at,
            'mark_read': request.data.get('mark_read', instance.mark_read),
        }
        
        serializer = RequestQuoteSerializer(instance, data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        response = {
            'status': 'success',
            'message': "Request Quote updated successfully",
        }
        
        return Response(response)

    def destroy(self, request, pk):
        instance = self.get_object(pk)
        instance.delete()
        response = {
            'status': 'success',
            'message': "Request Quote deleted successfully",
        }
        
        return Response(response)
