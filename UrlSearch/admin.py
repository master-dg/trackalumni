from django.contrib import admin
from .models import BasicInformation,CollegeDetails,Skills,PeriodicTask,TasksInfo
# Register your models here.

admin.site.register(BasicInformation)
admin.site.register(CollegeDetails)
admin.site.register(Skills)
admin.site.register(TasksInfo)
# admin.site.register(PeriodicTask)
