__author__ = 'zrc'
__date__ = '2019/7/1 9:50'

import django_filters
from django.db.models import Q

from .models import Grade


class GradeFilter(django_filters.rest_framework.FilterSet):
    GRADE_TYPE = (
        (1, '文科班'),
        (2, '理科班'),
        (3, '艺术班'),
    )
    name = django_filters.CharFilter(field_name='name', help_text="名称", lookup_expr='contains')
    type = django_filters.ChoiceFilter(field_name='profile__type', help_text="班级类型", choices=GRADE_TYPE)

    class Meta:
        model = Grade
        fields = ['name', 'type']