from django.db import models


class Grade(models.Model) :
    name = models.CharField(max_length=32, unique=True, verbose_name="班级名称")
    desc = models.CharField(max_length=1024, verbose_name="简介")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta :
        verbose_name = "年级班级"
        verbose_name_plural = verbose_name
        # unique_together = ('name', 'desc')

    def __str__(self) :
        return self.name


class GradeProfile(models.Model):
    GRADE_TYPE = (
        (1, '文科班'),
        (2, '理科班'),
        (3, '艺术班'),
    )
    grade = models.OneToOneField(Grade, on_delete=models.CASCADE, related_name='profile', verbose_name="班级")
    email = models.EmailField(max_length=64, verbose_name="邮箱")
    anniversary = models.DateField(verbose_name="班庆日")
    just_datetime = models.DateTimeField(verbose_name="日期时间")
    type = models.SmallIntegerField(choices=GRADE_TYPE, default=1, verbose_name="类型")
    star = models.IntegerField(default=0, verbose_name="星级")
    logo = models.ImageField(max_length=200, null=True, blank=True, upload_to="grade/logo/")
    info = models.TextField(null=True, blank=True, verbose_name="其他信息")

    class Meta :
        verbose_name = "班级档案"
        verbose_name_plural = verbose_name

    def __str__(self) :
        return self.email