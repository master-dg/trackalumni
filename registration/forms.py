

from .models import Database_Info
from users_auth.models import CustomUser
from .models import Database_Info
from django import forms


class CollegeAdminCreationForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ["email", "username", "first_name", "last_name", "phone_no"]


class CollegeDataBaseCreateForm(forms.ModelForm):

    class Meta:
        model = Database_Info
        fields = ["college_name", "db_name", "db_user",
                  "db_password", "db_host", "db_port"]
