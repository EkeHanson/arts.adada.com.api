from .views import RegisterView, LoginView, SendOTPView, VerifyOTPView

from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', RegisterView)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),

    # path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    # path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]