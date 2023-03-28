from django.contrib import admin
from .models import Department,Designation,College
# Register your models here.

admin.site.register(Department)
admin.site.register(Designation)


@admin.register(College)
class CollageAdmin(admin.ModelAdmin):
    list_display=['college_name','department_in','designation_in']
