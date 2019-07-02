"""MyProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.static import serve
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.documentation import include_docs_urls

from MyProject.settings import MEDIA_ROOT
from school.views import GradeViewSet, StudentViewSet, CourseViewSet
from school.view_tutorial import GradeListView, GradeListView2, GradeListView3, GradeListView4
from school.view_tutorial import GradeListAPIView, GradeListAPIView2
from school.view_tutorial import GradeGenericAPIView, GradeGenericAPIView2, GradeGenericAPIView3
from school.view_tutorial import GradViewSetTemp, GradeGenericViewSet
from school.view_user import UserViewSet

router = routers.DefaultRouter()
router.register("grades", GradeViewSet, "grades")
router.register("study/grades0", GradViewSetTemp, "grades0")
router.register("study/grades8", GradeGenericViewSet, "grades8")
router.register("students", StudentViewSet, "students")
router.register("courses", CourseViewSet, "courses")

router2 = routers.DefaultRouter()
router2.register("users", UserViewSet, "users")

urlpatterns = [
    path('admin/', admin.site.urls),

    # 配置上传文件的访问处理函数
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),

    path('api/', include(router.urls)),
    path('', include(router2.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # JWF 认证接口
    path('login/', obtain_jwt_token),
    path('docs/', include_docs_urls(title="ZRC")),

    path('study/grades/', GradeListView.as_view()),
    path('study/grades2/', GradeListView2.as_view()),
    path('study/grades3/', GradeListView3.as_view()),
    path('study/grades4/', GradeListView4.as_view()),

    path('study/grades5/', GradeListAPIView.as_view()),
    # re_path('^study/grades5/(?P<pk>[0-9]+)/$', GradeListAPIView2.as_view()),
    path('study/grades5/<int:pk>/', GradeListAPIView2.as_view()),

    path('study/grades6/', GradeGenericAPIView.as_view()),
    path('study/grades7/', GradeGenericAPIView2.as_view()),
    path('study/grades7/<int:pk>/', GradeGenericAPIView3.as_view())
]
