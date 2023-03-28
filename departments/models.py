from django.db import models

# Create your models here.

class Department(models.Model):
    department_name = models.CharField(max_length=30)
    dept_short_code = models.CharField(max_length=10, blank=True, null=True) 

    def __str__(self) -> str:
        return str(self.department_name)
    
    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'


class Designation(models.Model):
    designation = models.CharField(max_length=15)

    def __str__(self) -> str:
        return str(self.designation)

    class Meta:
        verbose_name = 'Designation'
        verbose_name_plural = 'Designations'



class College(models.Model):
    college_name=models.CharField(max_length=50,unique=True)
    college_short_code=models.CharField(max_length=10,unique=True,null=True)
    department_List=models.ManyToManyField(Department)
    designation_List = models.ManyToManyField(Designation)  
    
    def __str__(self) -> str:
        return str(self.college_name)

    def department_in(self):
        return ",".join([str(department) for department in self.department_List.all()])
    
    def designation_in(self):
        return ",".join([str(designation) for designation in self.designation_List.all()])

    class Meta:
        verbose_name = 'College'
        verbose_name_plural = 'Colleges'
