from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from decimal import Decimal
from .models import Category, Course, Instructors, MainCategory
from .serializers import  CategorySerializer, CourseSerializer, InstructorSerializer, MainCategorySerializer
from  .permissions import IsAdminUserType
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Allow any user to view the list or retrieve details
            return [IsAuthenticatedOrReadOnly()]
        # Require admin user type for any modifying actions
        return [IsAdminUserType()]


class InstructorsViewSet(viewsets.ModelViewSet):
    queryset = Instructors.objects.all()
    serializer_class = InstructorSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdminUserType()]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdminUserType()]


class MainCategoryViewSet(viewsets.ModelViewSet):
    queryset = MainCategory.objects.all()
    serializer_class = MainCategorySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticatedOrReadOnly()]
        return [IsAdminUserType()]
