from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import detail_route, list_route

from .models import Grade, Student, Course, StudentCourse
from .serializers import GradeSerializer, GradeSerializer2, StudentSerializer, CourseSerializer
from .serializers import StudentCourseListSerializer


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

    @list_route(methods=['get'])
    def list_student_course(self, request,format=None):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = StudentCourseListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = StudentCourseListSerializer(queryset, many=True)
        return Response(serializer.data)

    # @detail_route(methods=['get'])
    # def get_course(self, request, pk=None):
    #     student = self.get_object()
    #     courses = StudentCourse.objects.filter(student=student)
    #     serializer = StudentCourseSerializer(courses, many=True)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    @detail_route(methods=['post'])
    def set_course(self, request, pk=None):
        instance = self.get_object()

        new_courses = []
        if 'courses' in request.data:
            ids_new = []
            ids_pre = StudentCourse.objects.all().filter(student=instance).values_list('id', flat=True)
            for param in request.data.pop('courses'):
                param.pop("isSet", None)
                id = param.pop("id", None)
                course_data = param.pop("course")
                course = Course.objects.get(id=course_data['id'])
                param["student"] = instance
                param["course"] = course
                ans, _created = StudentCourse.objects.update_or_create(id=id, defaults={**param})
                ids_new.append(ans.id)
                new_courses.append(ans)

            delete_ids = set(ids_pre) - set(ids_new)
            StudentCourse.objects.filter(id__in=delete_ids).delete()
        serializer = StudentCourseListSerializer(instance,many=False)
        return Response(serializer.data)


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = GradePagination
