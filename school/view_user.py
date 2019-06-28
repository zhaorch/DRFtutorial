from django.contrib.auth import get_user_model
from rest_framework import viewsets,serializers
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions
from rest_framework.decorators import detail_route


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    用户
    """
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, authentication.SessionAuthentication )
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # /users/{pk}/userInfo/
    @detail_route(methods=['get'])
    def userInfo(self, request, pk=None):
        user =request.user
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)