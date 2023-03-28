from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Permission(models.Model):
    PERMISSION_LIST=(
        (1,_("Gave Permssion To SuperUser")),
        (2,_("Gave Permmison To User")),
        (3,_("Search Data From DataBase")),
        (4,_("Analyze Data")),
        (5,_("Download Data File")),
    )
    permission_name=models.CharField(choices=PERMISSION_LIST,default= 3,max_length=2)

    def __str__(self) -> str:
        return str(self.get_permission_name_dispaly)
    
    class Meta:
        verbose_name = 'Permission'
        verbose_name_plural = 'Permissions'

    
class Role(models.Model):
    class Role_List(models.TextChoices):
        ADMIN='admin',_("Admin")
        SUPERUSER = 'superuser', _("SuperUser")
        USER='user',_("User")
        ENDUSER='end_user',_("EndUser")

    role_name = models.CharField(max_length=10,choices=Role_List.choices,default=Role_List.USER)
    permissions = models.ManyToManyField(Permission)

    def __str__(self) -> str:
        return str(self.role_name)
    
    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'


