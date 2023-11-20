from rest_framework import serializers

from authentication.models import User, VendorModel

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'state', 'first_time']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorModel
        fields = ['id', 'user', 'pancard', 'gst', 'proof_of_registration', 'approved']
