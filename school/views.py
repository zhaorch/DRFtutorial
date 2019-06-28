from rest_framework import viewsets

from .models import Grade
from .serializers import GradeSerializer,GradeSerializer2


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
