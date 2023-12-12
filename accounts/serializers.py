from rest_framework import serializers

from authentication.models import User, VendorModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'user_type', 'last_name', 'state', 'first_time', 'profile_photo', 'phone_number']

class VendorSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    
    def get_user(self, obj):
        return UserSerializer(obj.user).data
    
    class Meta:
        model = VendorModel
        fields = ['id', 'user', 'pancard', 'gst', 'proof_of_registration', 'approved', 'address', 'website', 'date_of_incorporation']
        
class VendorCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorModel
        fields = ['id', 'user', 'pancard', 'gst', 'proof_of_registration', 'approved', 'address', 'website', 'date_of_incorporation']
