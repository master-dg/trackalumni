from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from users_auth.models import CustomUser
from departments.models import College
from django.conf import settings
from TrackYourAlumni.settings import DATABASE_STORE_ENTRY
# Create your models here.
class DataBaseManager(models.Manager):
    using =DATABASE_STORE_ENTRY


class Database_Info(models.Model):
    
    db_creator = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True,blank=True)
    college_name=models.CharField(max_length=30,null=True)
    db_name=models.CharField(max_length=30,null=True,blank=True)
    db_user=models.CharField(max_length=30, null=True,blank=True)
    db_password=models.CharField(max_length=15, null=True,blank=True)
    db_host=models.CharField(max_length=100, null=True,blank=True)
    db_port=models.CharField(max_length=15,null=True,blank=True)

    def __str__(self):
        return str(self.college_name)

    class Meta:
        

        db_table = 'Database_Info'
        managed = True
        verbose_name = 'Database_Info'
        verbose_name_plural = 'Database_Infos'
        unique_together = [('college_name', 'db_name'),('db_name','db_user') ]
      
    

        
