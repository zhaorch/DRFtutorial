from django.contrib import admin

from .models import Grade


class GradeAdmin(admin.ModelAdmin):
    list_display = ["name", "desc", "created_time", "updated_time"]
    list_filter = ["name",]
    search_fields = ['name',]


admin.site.register(Grade, GradeAdmin)
