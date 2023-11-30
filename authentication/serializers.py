from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from authentication.models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username','password', 'email', 'first_name', 'last_name', 'user_type', 'phone_number', 'state', 'profile_photo')
        extra_kwargs = {
            'password': {'write_only': True, 'required': True, 'validators': [validate_password]},
            'email': {'required': True, 'validators': [UniqueValidator(queryset=User.objects.all())]},
            'phone_number': {'required': True, 'validators': [UniqueValidator(queryset=User.objects.all())]},
            'first_name': {'required': True},
            'last_name': {'required': True}
            }
        
    def create(self, validated_data):
        user_type = validated_data.get('user_type', 'end_consumer')
        user = User.objects.create(
            username = validated_data.get('username', "default"),
            email = validated_data['email'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            phone_number = validated_data['phone_number'],
            user_type = user_type,
            state = validated_data.get('state'),
            profile_photo = validated_data.get('profile_photo'),
        )
        
        user.set_password(validated_data['password'])
        user.save()
        
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            'password', 'last_login', 'is_active', 'is_superuser', 'is_staff',
            'groups', 'user_permissions', 'date_joined',
        )

class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)