from django.urls import path
from .views import RegisterView, LoginView, SendOTPView, VerifyOTPView

urlpatterns = [
    path('users/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
]
