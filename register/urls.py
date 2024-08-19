from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, LoginView
#, PasswordResetRequestView, PasswordResetConfirmView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),

    # path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    # path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
