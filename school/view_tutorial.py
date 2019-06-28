import json
from django.views import View
from django.http import HttpResponse, JsonResponse, Http404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics, viewsets, permissions
from rest_framework.pagination import PageNumberPagination

from .serializers import GradeSerializer
from .models import Grade

# -----------------------------------------------------------------


class GradeListView(View):
    def get(self,request):
        grades = Grade.objects.all()[:5]

        json_list = []
        for grade in grades:
            json_dict = dict()
            json_dict['name'] = grade.name
            json_dict['desc'] = grade.desc
            # json_dict['created_time'] = good.created_time  # 日期没法序列化
            json_list.append(json_dict)

        return HttpResponse(json.dumps(json_list,ensure_ascii=False),content_type='application/json,charset=utf-8')


class GradeListView2(View):
    def get(self,request):
        grades = Grade.objects.all()[:5]

        from django.forms.models import model_to_dict
        json_list = []
        for grade in grades:
            json_dict = model_to_dict(grade)  # ImageField 无法序列化
            json_list.append(json_dict)

        return HttpResponse(json.dumps(json_list,ensure_ascii=False),content_type='application/json,charset=utf-8')


class GradeListView3(View):
    def get(self,request):
        grades = Grade.objects.all()[:5]

        from django.core import serializers
        json_data = serializers.serialize('json', grades, ensure_ascii=False)

        return HttpResponse(json_data, content_type='application/json,charset=utf-8')


class GradeListView4(View):
    def get(self,request):
        grades = Grade.objects.all()[:5]

        from django.core import serializers
        json_data = serializers.serialize('json', grades, ensure_ascii=False)
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False, json_dumps_params={'ensure_ascii' : False})

# -----------------------------------------------------------------


class GradeListAPIView(APIView):
    def get(self, request, format=None):
        grades = Grade.objects.all()[:5]
        # serializer = GradeSerializer(instance=grades, many=True)
        serializer = GradeSerializer(grades, many=True)
        return Response(serializer.data)
        # return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii' : False})

    def post(self, request, format=None):
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GradeListAPIView2(APIView):
    def get_object(self, pk):
        try:
            return Grade.objects.get(pk=pk)
        except Grade.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        grade = self.get_object(pk)
        serializer = GradeSerializer(grade)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        grade = self.get_object(pk)
        serializer = GradeSerializer(grade, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        grade = self.get_object(pk)
        grade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -----------------------------------------------------------------


class GoodsPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class GradeGenericAPIView(mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    pagination_class = GoodsPagination


    def get(self, request, *args, **kwargs) :
        return self.list(request, *args, **kwargs)


class GradeGenericAPIView2(generics.ListAPIView, generics.CreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    pagination_class = GoodsPagination


class GradeGenericAPIView3(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

# -----------------------------------------------------------------


class GradViewSetTemp(viewsets.ViewSet):
    def list(self, request):
        queryset = Grade.objects.all()
        serializer = GradeSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = GradeSerializer(data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        grade = Grade.objects.get(pk=pk)
        serializer = GradeSerializer(grade)
        return Response(serializer.data)

    def update(self, request, pk=None):
        grade = self.get_object(pk)
        serializer = GradeSerializer(grade, data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        grade = self.get_object(pk)
        serializer = GradeSerializer(grade, data=request.data)
        if serializer.is_valid() :
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        grade = self.get_object(pk)
        grade.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -----------------------------------------------------------------


from rest_framework.decorators import action,detail_route,list_route


# class GradeGenericViewSet(viewsets.ModelViewSet): 可简写为ModelViewSet,继承了增删改查的所有方法
class GradeGenericViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,mixins.CreateModelMixin,
                          mixins.UpdateModelMixin,mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    pagination_class = GoodsPagination

    #@action(methods=['get'], detail=True, url_path='info', url_name='detail')
    @detail_route(methods=['get'], url_path='info', url_name='detail')
    def get_grade_info(self, request, pk=None):
        grade = self.get_object()
        serializer = GradeSerializer(grade, many=False)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    # @detail_route(methods=['get'], url_path='info2', url_name='info2')
    @list_route(methods=['get'], url_path='info2', url_name='info2')
    def get_grade_info2(self, request, pk=None) :
        json_list = []
        for i in range(10):
            json_dict = dict()
            json_dict['name'] = i
            json_dict['desc'] = i+1000
            json_list.append(json_dict)
        return Response([temp['desc'] for temp in json_list], status=status.HTTP_200_OK)

    @list_route(methods=['get'], url_path='clist', url_name='detail')
    def get_grade_list(self,request):
        name = request.query_params.get("name", '')
        list = Grade.objects.filter(name__contains=name)
        serializer = GradeSerializer(list, many=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)



