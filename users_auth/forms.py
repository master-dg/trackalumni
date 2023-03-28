from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import  AuthenticationForm as BaseAuthenticationForm
from .models import CustomUser, College
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm as BaseAuthenticationForm,
    SetPasswordForm as BaseSetPasswordForm,
    PasswordChangeForm as BasePasswordChangeForm,
    PasswordResetForm,
)
from django.utils.translation import gettext_lazy as _
import re
from django.core.exceptions import ValidationError

class AuthenticationForm(BaseAuthenticationForm):
    college_name = forms.ModelChoiceField(queryset=College.objects.all().values(), initial=0, label="Select College")
    class Meta:
        model = CustomUser
        fields = ["username", "password", "college_name"]

       
class SetPasswordForm(BaseSetPasswordForm):
    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get("new_password1")

        if not re.findall("\d", new_password1):
            self.add_error(
                "new_password1", _("The password must contain at least one digit, 0-9.")
            )

        if not re.findall("[A-Z]", new_password1):
            self.add_error(
                "new_password1",
                _("The password must contain at least 1 uppercase letter, A-Z."),
            )

        if not re.findall("[a-z]", new_password1):
            self.add_error(
                "new_password1",
                _("The password must contain at least 1 lowercase letter, a-z."),
            )

        if not re.findall("[~!@#$%^&*_]", new_password1):
            self.add_error(
                "new_password1",
                _("The password must contain at least 1 symbol: ~!@#$%^&*_"),
            )

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit)
        user.is_active = True
        user.save()
        return user


class PasswordChangeForm(BasePasswordChangeForm, SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        BasePasswordChangeForm.__init__(self, user, *args, **kwargs)
        SetPasswordForm.__init__(self, user, *args, **kwargs)


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields =["email","username","first_name","last_name","role","college_name","department","designation","phone_no"]

    def save(self, commit=None):
        user = super(UserCreateForm, self).save(commit=False)
        user.is_superuser = False
        if str(self.cleaned_data["role"]) == CustomUser.Role.ADMIN.value:
            user.is_superuser = True
            user.is_role_admin = True
        if str(self.cleaned_data["role"]) == CustomUser.Role.SUPERUSER.value:
            user.is_role_superuser = True
        if str(self.cleaned_data["role"]) == CustomUser.Role.USER.value:
            user.is_role_user = True
        user.is_verified=False
        user.is_active = True
        user.save()
        # if "profile_image" in self.cleaned_data:
        #     profile_image = self.cleaned_data.pop("profile_image")
        #     user.profile_image = profile_image
        #     user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["email","username","first_name","last_name","role","college_name","department","designation","phone_no"]


class EmailValidationOnForgotPassword(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        if not CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError(
                _("There is no user registered with the specified email address!")
            )
        return email
