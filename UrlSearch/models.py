from django.db import models
from departments.models import Department,College
from django_celery_beat.models import PeriodicTask as BasePeriodicTask
from TrackYourAlumni.models import BaseModel
from django_celery_results.models import TaskResult
from users_auth.models import CustomUser

#Database Models 
# Basic Information 
class BasicInformation(models.Model):
    PublicId = models.CharField(unique= True,max_length=100, null=True)
    FirstName = models.CharField(max_length=100,null=True)
    LastName = models.CharField(max_length=100,null=True)
    Address = models.CharField(max_length=100,null=True)
    Country= models.CharField(max_length=20,null=True)
    Field = models.CharField(max_length=100,null=True)
    department=models.CharField(max_length=50,null=True)
    batch_year=models.CharField(max_length=4,null=True)
    college_id=models.CharField(max_length=15,null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True,null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True,null=True)

    def __str__(self):
        return str(self.PublicId)

#College Details
class CollegeDetails(models.Model):
    PublicId = models.ForeignKey( BasicInformation, on_delete= models.CASCADE, related_name="student_college_details")
    CollegeName = models.CharField(max_length=100)
    CollegeCity = models.CharField(max_length=100,null=True)
    CollegeState = models.CharField(max_length=100,null=True)
    CollegeCountry = models.CharField(max_length=100,null=True)
    CollegeContinent = models.CharField(max_length=100,null=True)
    DegreeName = models.CharField(max_length=100,null=True)
    StartYear = models.CharField(max_length=15,null=True)
    EndYear = models.CharField(max_length=15,null=True)

    
    def __str__(self):
        return str(self.PublicId)

#Skills
class Skills(models.Model):
    PublicId = models.ForeignKey(BasicInformation, on_delete=models.CASCADE, null=True, related_name="student_skills")
    SkillName = models.CharField(max_length=80)

    def __str__(self):
        return str(self.PublicId)

#CompanyDetails 
class CompanyDetails(models.Model):
    PublicId = models.ForeignKey( BasicInformation, on_delete= models.CASCADE, related_name="student_company_details")
    JobTitle = models.CharField(max_length=100,null=True)
    c_StartYear = models.CharField(max_length=15,null=True)
    c_EndYear = models.CharField(max_length=15,null=True)
    CompanyName = models.CharField(max_length=100,null=True)
    CompanyCity = models.CharField(max_length=100,null=True)
    CompanyState = models.CharField(max_length=100,null=True)
    CompanyCountry = models.CharField(max_length=100,null=True)
    CompanyContinent = models.CharField(max_length=100,null=True)

    def __str__(self):
        return str(self.PublicId)


class PeriodicTask(BasePeriodicTask):
    task_name=models.CharField(max_length=100,unique=True,null=True)
    department=models.ForeignKey(Department, on_delete=models.PROTECT,related_name= "task_department",null=True)
    days=models.IntegerField(null=True)
    batch_year=models.CharField(max_length=4,null=True)
    college_name=models.ForeignKey(College, on_delete= models.PROTECT, related_name= "task_college",null=True)

    # class Meta:
    #     app_label='django_celery_beat'



class TasksInfo(models.Model):
    task=models.CharField(max_length=255,null=True)
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True)
    file=models.FileField(null=True)
    college_name=models.ForeignKey(College,on_delete=models.CASCADE,null=True)
    task_name=models.CharField(max_length=50,null=True)

    def __str__(self):
        return str(self.task)