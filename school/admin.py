from django.contrib import admin

from .models import Grade,GradeProfile


class GradeAdmin(admin.ModelAdmin):
    list_display = ["name", "desc", "created_time", "updated_time"]
    list_filter = ["name",]
    search_fields = ['name',]


class GradeProfileAdmin(admin.ModelAdmin):
    list_display = ["email", "info"]
    list_filter = ["email",]
    search_fields = ['email',]

admin.site.register(Grade, GradeAdmin)
admin.site.register(GradeProfile, GradeProfileAdmin)
