from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
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


class SearchCourseView(APIView):
    # Override permission_classes to allow unrestricted access
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        search_term = request.query_params.get('q', None)
        if not search_term:
            return Response({"error": "Please provide a search term."}, status=status.HTTP_400_BAD_REQUEST)

        # Find courses matching the search term
        courses = Course.objects.filter(title__icontains=search_term)

        if not courses.exists():
            return Response({"error": "No courses found."}, status=status.HTTP_404_NOT_FOUND)

        # Get the unique categories associated with these courses
        categories = Category.objects.filter(courses__in=courses).distinct()

        # Serialize the categories along with their courses
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)