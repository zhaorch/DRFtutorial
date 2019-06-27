__author__ = 'zrc'
__date__ = '2019/6/27 9:34'

from rest_framework import serializers

from .models import Grade


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = "__all__"
