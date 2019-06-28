__author__ = 'zrc'
__date__ = '2019/6/27 9:34'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Grade,GradeProfile


def CommonValidate(value):
    if '高' not in value or '班' not in value :
        raise serializers.ValidationError('名称必须包含高/班')


class GradeProfileSerializer(serializers.ModelSerializer):
    just_datetime = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = GradeProfile
        fields = "__all__"


class GradeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=32, validators=[CommonValidate])
    created_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    profile = GradeProfileSerializer(many=False)

    def validate_desc(self, value):
        if '高' not in value.lower():
            raise serializers.ValidationError("简介必须包含【高】字")
        return value

    def validate(self, data):
        if data['name'] not in data['desc']:
            raise serializers.ValidationError("简介必须包含名称")
        return data

    class Meta:
        model = Grade
        fields = "__all__"
        validators = [UniqueTogetherValidator(
                queryset=Grade.objects.all(),
                fields=['name', 'desc'],
                message='名字和简介必须唯一')]


class GradeSerializer2(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=32)
    desc = serializers.CharField(max_length=1024)
    created_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    def create(self, validated_data) :
        return Grade.objects.create(**validated_data)

    def update(self, instance, validated_data) :
        instance.name = validated_data.get('name', instance.name)
        instance.desc = validated_data.get('desc', instance.desc)
        instance.save()
        return instance
