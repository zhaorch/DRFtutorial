from rest_framework import viewsets, mixins, status, permissions, authentication, filters
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import detail_route, list_route
from rest_framework_extensions.mixins import PaginateByMaxMixin
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework_extensions.cache.mixins import CacheResponseMixin

from .models import Grade, Student, Course, StudentCourse
from .serializers import GradeSerializer, GradeSerializer2, StudentSerializer, CourseSerializer
from .serializers import StudentCourseListSerializer
from .filters import GradeFilter


class CommonPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'
    page_query_param = "page"
    max_page_size = 100


class CommonPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        a = request.resolver_match.url_name
        return request.user.is_superuser == 1


class ZRCRateThrottle(UserRateThrottle):
    scope = 'zrc'


#class GradeViewSet(CacheResponseMixin, viewsets.ModelViewSet):
class GradeViewSet(viewsets.ModelViewSet) :
    queryset = Grade.objects.all().select_related("profile").order_by("created_time")
    serializer_class = GradeSerializer
    pagination_class = CommonPagination

    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, CommonPermission)
    # authentication_classes = (authentication.BasicAuthentication, authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filter_class = GradeFilter
    search_fields = ('name', 'profile__email')
    ordering_fields = ('name',)
    # throttle_classes = (UserRateThrottle,)
    # throttle_classes = (ZRCRateThrottle, AnonRateThrottle, ScopedRateThrottle)
    # throttle_scope = 'abc'
    throttle_classes = (UserRateThrottle, AnonRateThrottle)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    pagination_class = CommonPagination

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
                course = Course(**course_data)
                # course = Course.objects.get(id=course_data['id'])
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
    pagination_class = CommonPagination
