from rest_framework import serializers
from .models import CustomUser


class SendOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
class VerifyOTPSerializer(serializers.Serializer):
    otp_session_id = serializers.CharField(max_length=255)
    otp_entered_by_user = serializers.CharField(max_length=6)


class UserRegistrationSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(default='student')
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'full_name', 'password']
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            phone=validated_data['phone'],
            full_name=validated_data['full_name'],
            password=validated_data['password']
        )
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
