from django.db import models
from tinymce.models import HTMLField


class Grade(models.Model):
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
    grade = models.OneToOneField(Grade, on_delete=models.CASCADE, null=True, blank=True, related_name='profile', verbose_name="班级")
    email = models.EmailField(max_length=64, verbose_name="邮箱")
    anniversary = models.DateField(verbose_name="班庆日")
    just_datetime = models.DateTimeField(verbose_name="日期时间")
    type = models.SmallIntegerField(choices=GRADE_TYPE, default=1, verbose_name="类型")
    star = models.IntegerField(default=0, verbose_name="星级")
    logo = models.ImageField(max_length=200, null=True, blank=True, upload_to="grade/logo/")
    # info = models.TextField(null=True, blank=True, verbose_name="其他信息")
    info = HTMLField(null=True, blank=True, verbose_name="其他信息")

    class Meta :
        verbose_name = "班级档案"
        verbose_name_plural = verbose_name

    def __str__(self) :
        return self.email


class Student(models.Model):
    no = models.CharField(max_length=32, unique=True, verbose_name="学号")
    name = models.CharField(max_length=32, verbose_name="姓名")
    gender = models.BooleanField(default=0, verbose_name="性别")
    birthday = models.DateField(null=True, blank=True, verbose_name="出生年月")
    grade = models.ForeignKey(Grade, verbose_name="班级", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "学生"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}({1})".format(self.name, self.no)


class StudentGoods(models.Model):
    name = models.CharField(max_length=32, verbose_name="名称")
    price = models.FloatField(default=0, verbose_name="单价")
    number = models.PositiveIntegerField(default=1, verbose_name="数量")
    student = models.ForeignKey(Student, verbose_name="归属", null=True, blank=True, related_name="goods", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "学生物品"
        verbose_name_plural = verbose_name
        unique_together = ('name', 'student')

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=32, unique=True, verbose_name='课程名称')
    desc = models.CharField(max_length=1024, verbose_name="简介")

    class Meta :
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class StudentCourse(models.Model):
    student = models.ForeignKey(Student, verbose_name="学生", null=True, blank=True, related_name='courses', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, verbose_name="课程", null=True, blank=True, on_delete=models.CASCADE)
    desc = models.CharField(max_length=1024, verbose_name="其他信息")

    class Meta :
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}-{1}".format(self.student, self.course)