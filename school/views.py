from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .models import Grade, Student
from .serializers import GradeSerializer, GradeSerializer2, StudentSerializer


class GradePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    page_query_param = "page"
    max_page_size = 100


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    pagination_class = GradePagination


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = GradePagination
