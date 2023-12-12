from rest_framework import serializers

from notifications.models import Notification, Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'message']
        
class NotificationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['user', 'message', 'title']
        
class NotificationSerializer(serializers.ModelSerializer):
    message = MessageSerializer()
    user = serializers.SerializerMethodField()
    
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'title', 'created_at', 'mark_read']
        
    def get_user(request, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
