from django.db import models

from phonenumber_field.modelfields import PhoneNumberField
from departments.models import Department,Designation, College 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager


class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    class Role(models.TextChoices):
        ADMIN = "ADMIN"
        SUPERUSER = "SUPERUSER"
        USER = "USER"
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    username=models.CharField(max_length=10,unique=True,null=True)
    first_name=models.CharField(max_length=50,null=True)
    last_name=models.CharField(max_length=50,null=True)
    phone_no =PhoneNumberField(null=True)

    college_name=models.ForeignKey(College, on_delete= models.PROTECT, related_name= "user_college",null=True)
    department=models.ForeignKey(Department, on_delete=models.PROTECT, related_name= "user_department",null=True)
    designation=models.ForeignKey(Designation, on_delete=models.PROTECT,  related_name="user_designation",null=True)

    is_verified=models.BooleanField(default=False)
    verified_by=models.CharField(max_length=10,null=True,blank=True)

    date_joined=models.DateTimeField(auto_now=True,null=True,blank=True)
    date_profile_updated=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    is_role_admin=models.BooleanField(default=False)
    is_role_superuser=models.BooleanField(default=False)
    is_role_user=models.BooleanField(default=False)


    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    class Meta:
        unique_together = ['email','username','first_name']
        verbose_name = 'CustomUser'
        verbose_name_plural = 'CustomUsers'

