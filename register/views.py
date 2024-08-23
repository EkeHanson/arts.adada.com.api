from rest_framework import viewsets, status, views, generics
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, SendOTPSerializer, VerifyOTPSerializer
from rest_framework.permissions import AllowAny
import requests
from django.conf import settings
from rest_framework.decorators import action
from django.core.exceptions import ObjectDoesNotExist


class SendOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SendOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data['phone_number']

        # Check if user exists with that phone number
        try:
            user = CustomUser.objects.get(phone=phone_number)
        except ObjectDoesNotExist:
            return Response({'detail': 'User with this phone number does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        # Generate OTP (you can generate a random OTP here)
        otp_value = '123456'  # Replace with a method to generate a dynamic OTP
        otp_template_name = 'OTP_Template_Name'  # Replace with your actual template name

        # Make a request to 2factor API to send OTP
        url = f'https://2factor.in/API/V1/{settings.TWO_FACTOR_API_KEY}/SMS/{phone_number}/{otp_value}/{otp_template_name}'
        response = requests.get(url)

        if response.status_code == 200:
            # You can store the OTP session ID if needed for verification
            otp_session_id = response.json().get('Details')
            return Response({'message': 'OTP sent successfully', 'otp_session_id': otp_session_id}, status=status.HTTP_200_OK)
        return Response({'detail': 'Failed to send OTP'}, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = VerifyOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_session_id = serializer.validated_data['otp_session_id']
        otp_entered_by_user = serializer.validated_data['otp_entered_by_user']

        # Make a request to 2factor API to verify OTP
        url = f'https://2factor.in/API/V1/{settings.TWO_FACTOR_API_KEY}/SMS/VERIFY/{otp_session_id}/{otp_entered_by_user}'
        response = requests.get(url)

        if response.status_code == 200 and response.json().get('Details') == 'OTP Matched':
            return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)



class RegisterView(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all().order_by('-id')  # LIFO principle
    serializer_class = UserRegistrationSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if not serializer.is_valid():
            # Log the specific errors for debugging
            print(f"PATCH request errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-type/(?P<type>[^/.]+)')
    def get_users_by_type(self, request, level=None):
        if level not in ['CLIENT', 'ADMIN']:
            return Response({"error": "Invalid Type"}, status=status.HTTP_400_BAD_REQUEST)
        
        users = CustomUser.objects.filter(level=level).order_by('-id')  # LIFO principle
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]  # Allow unauthenticated access

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(email=email, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'email': user.email,
                'user_type': user.user_type,
                'full_name': user.full_name,
                'date_joined': user.date_joined,
            })
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
