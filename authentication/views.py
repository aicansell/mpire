from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from authentication.models import EmailConfirmationToken, User

from authentication.serializers import RegisterSerializer, LoginSerializer, ChangePasswordSerializer
from authentication.utils import send_email

class RegisterViewSet(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginViewSet(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
    
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
            
        if user is not None and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            user_data = LoginSerializer(user).data
                
            response = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': user_data
            }
                
            return Response(response, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
class ChangePasswordViewSet(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get('old_password')
            
            if user.check_password(old_password):
                new_password = serializer.data.get('new_password')
                if old_password == new_password:
                    return Response({'message': 'New password cannot be same as old password'}, status=status.HTTP_400_BAD_REQUEST)
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmailVerificationViewSet(APIView):
    def get(self, request):
        token = request.query_params.get('token')
        
        try:
            token = EmailConfirmationToken.objects.get(id=token)
            user = token.user
            user.is_emailverified = True
            user.save()
            token.delete()
            return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
        except EmailConfirmationToken.DoesNotExist:
            return Response({'message': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
        
        if user.is_emailverified:
            return Response({'message': 'Email is already verified.'}, status=status.HTTP_200_OK)
        
        try:
            token = EmailConfirmationToken.objects.get(user=user)
        except:
            token = EmailConfirmationToken.objects.create(user=user)
            token.save()
            
        verification_url = f"http://localhost:8000/verify/?token={token.id}"

        data = {
            'name': user.first_name + ' ' + user.last_name,
            'link': verification_url,
        }
        
        send_email(
            template_name="email_confirmation_mail.txt",
            data=data,
            subject="Email Verification",
            to=[user.email]
        )
        return Response({'message' : 'A verification mail has been sent to registered email id.'},status=status.HTTP_200_OK)
