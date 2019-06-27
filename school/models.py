from django.db import models


class Grade(models.Model) :
    name = models.CharField(max_length=32, unique=True, verbose_name="年级班级名称")
    desc = models.CharField(max_length=1024, verbose_name="简介")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta :
        verbose_name = "年级班级"
        verbose_name_plural = verbose_name

    def __str__(self) :
        return self.name
