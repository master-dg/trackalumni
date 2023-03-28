from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from .forms import UserCreateForm, UserUpdateForm
from django.utils.translation import gettext_lazy as _
# Register your models here.

class UserAuthAdmin(UserAdmin):   
    form = UserUpdateForm 
    add_form = UserCreateForm
    model = CustomUser
    list_display=['username','first_name','last_name','email','role','college_name','department','designation','is_verified','is_role_admin','is_role_superuser','is_role_user','is_staff','is_active','is_superuser']
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_superuser', 'is_active', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Additional information'), {'fields': ('role', 'phone_no', 'college_name', 'department', 'designation','is_verified','verified_by','is_role_admin','is_role_superuser','is_role_user')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'is_staff', 'is_superuser', 'is_active', 'role', 'phone_no', 'college_name', 'department', 'designation','is_verified','is_role_admin','is_role_superuser','is_role_user')}
        ),
    )

admin.site.register(CustomUser,UserAuthAdmin)


# admin.site.register(CustomUser)
# admin.site.register(BaseClass)
