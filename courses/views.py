from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from decimal import Decimal
from .models import Category, Course, Instructors
from .serializers import  CategorySerializer, CourseSerializer, InstructorSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]


class InstructorsViewSet(viewsets.ModelViewSet):
    queryset = Instructors.objects.all()
    serializer_class = InstructorSerializer
    permission_classes = [AllowAny]


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

