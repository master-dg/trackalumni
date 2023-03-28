from django.db import models
from users_auth.models import CustomUser

class BaseModel(models.Model):
    created_by  = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    updated_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True
    

