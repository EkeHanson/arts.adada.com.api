from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, InstructorsViewSet, CategoryViewSet
#, PasswordResetRequestView, PasswordResetConfirmView

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'instructors', InstructorsViewSet)
router.register(r'category', CategoryViewSet)

urlpatterns = [
    path('', include(router.urls))

]
