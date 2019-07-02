__author__ = 'zrc'
__date__ = '2019/6/27 9:34'

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.db import transaction

from .models import Grade, GradeProfile, Student, StudentGoods, Course, StudentCourse


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension


def common_validate(value):
    if '高' not in value or '班' not in value :
        raise serializers.ValidationError('名称必须包含高/班')


class GradeProfileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)
    just_datetime = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')
    logo = Base64ImageField(max_length=None, use_url=True, allow_empty_file=True, allow_null=True)

    class Meta:
        model = GradeProfile
        # fields = "__all__"
        exclude = ('grade',)


class GradeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=32, validators=[common_validate])
    created_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    updated_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')
    profile = GradeProfileSerializer()

    def validate_desc(self, value):
        if '高' not in value.lower():
            raise serializers.ValidationError("简介必须包含【高】字")
        return value

    def validate(self, data):
        if data['name'] not in data['desc']:
            raise serializers.ValidationError("简介必须包含名称")
        return data

    @transaction.atomic
    def create(self, validated_data):
        profile_data = validated_data.pop("profile")
        grade = Grade.objects.create(**validated_data)
        GradeProfile.objects.create(grade=grade, **profile_data)
        return grade

    @transaction.atomic
    def update(self, instance, validated_data) :
        profile_data = validated_data.pop('profile')

        from rest_framework.utils import model_meta
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items() :
            if attr in info.relations and info.relations[attr].to_many :
                field = getattr(instance, attr)
                field.set(value)
            else :
                setattr(instance, attr, value)
        instance.save()

        id = profile_data.pop("id", None)
        profile_data['grade']=instance
        # id = None
        # if instance.profile:
        #     id = instance.profile.id
        new_profile, _created = GradeProfile.objects.update_or_create(id=id, defaults={**profile_data})
        instance.profile = new_profile

        return instance

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


class StudentGoodsSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=False, required=False)

    class Meta:
        model = StudentGoods
        exclude = ('student',)


class StudentSerializer(serializers.ModelSerializer):
    goods = StudentGoodsSerializer(many=True)

    class Meta:
        model = Student
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        goods_list = validated_data.pop("goods")
        instance = Student.objects.create(**validated_data)

        new_goods = []
        for goods in goods_list:
            new_goods.append(StudentGoods.objects.create(student=instance, **goods))

        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        new_goods = []
        if 'goods' in validated_data:
            ids_new = []
            ids_pre = StudentGoods.objects.all().filter(student=instance).values_list('id', flat=True)
            for param in validated_data.pop('goods'):
                param["student"] = instance
                id = param.pop("id", None)
                ans, _created = StudentGoods.objects.update_or_create(id=id, defaults={**param})
                ids_new.append(ans.id)
                new_goods.append(ans)

            delete_ids = set(ids_pre) - set(ids_new)
            StudentGoods.objects.filter(id__in=delete_ids).delete()

        from rest_framework.utils import model_meta
        info = model_meta.get_field_info(instance)
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


# ---------------------------
# class StudentNameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Student
#         fields = ('id', 'name')


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class StudentCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer(many=False)

    class Meta:
        model = StudentCourse
        fields = "__all__"


class StudentCourseListSerializer(serializers.ModelSerializer):
    courses = StudentCourseSerializer(many=True)
    grade = GradeSerializer(many=False, read_only=True)

    class Meta:
        model = Student
        fields = "__all__"



