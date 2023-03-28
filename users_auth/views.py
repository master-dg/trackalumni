from django.shortcuts import render, redirect
from .models import CustomUser
from django.views.generic import ListView
from .models import CustomUser
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView as BaseLoginView
from users_auth.forms import AuthenticationForm
from departments.models import College
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseRedirect,HttpResponse
from .forms import UserCreateForm
from django.forms.models import model_to_dict
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordResetView
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from users_auth.models import CustomUser
from users_auth.forms import (
    EmailValidationOnForgotPassword,
    UserCreateForm,
    PasswordChangeForm,
    UserUpdateForm,
)
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import PasswordChangeView
from django.http import JsonResponse
from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    UpdateView,
    RedirectView,
)
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.core.mail import BadHeaderError
from registration.utils import send_invitation
from django.contrib.sites.shortcuts import get_current_site
import smtplib
from django.template.loader import render_to_string
from django.core.mail import send_mail
from TrackYourAlumni.settings import DEFAULT_FROM_EMAIL

# Create your views here.
##TODO: CRUD operations of User, user-profile, change password, login , registration 

def get_department_designation(request, college_id):
    college_obj=College.objects.filter(id=college_id).first()
    department_list = [model_to_dict(department, fields=['id','department_name']) for department in list(college_obj.department_List.all())]
    desigantion_list = [model_to_dict(designation, fields=['id','designation']) for designation in list(college_obj.designation_List.all())]
    return JsonResponse({"dept_list":department_list,"desg_list":desigantion_list})

class LoginView(BaseLoginView):
    form_class = AuthenticationForm
    template_name = "registration/login.html"
    success_url = reverse_lazy("users_auth:user-list")
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs, college_list= list(College.objects.all().values()))
        return context

    def form_valid(self, form):
        self.get_context_data()
        user_email = form.cleaned_data.get("username")
        user = get_object_or_404(CustomUser, email = user_email)
        
        if user.is_authenticated and user.is_verified:
            user.is_active  = True
            success_url = super(LoginView, self).form_valid(form)
            update_session_auth_hash(self.request,user)
            if user.is_role_admin or user.is_role_superuser:
                return success_url
            else: 
                return redirect(reverse_lazy("dashboard:basic-info-list"))

        messages.error(self.request, "You are not verified user. Please wait until you get an email from higher authorities.")
        return render(self.request, "registration/login.html",context = self.get_context_data())




class ResetPasswordView(PasswordResetView):
    form_class = EmailValidationOnForgotPassword
    template_name = "registration/forgot_password.html"
    html_email_template_name = "registration/password_reset_email.html"
    email_template_name = "registration/password_reset_email.html"

    def post(self, request, *args, **kwargs):
        user_mail = request.POST.get("email", None)
        form = self.form_class(data=self.request.POST)
        if form.is_valid():
            subject_content = "Welcome To TrackAlumni! Reset Your Password"
            mail_template= "password_reset_email.html"
            try:
                send_invitation(self, self.request, user_mail, subject_content, mail_template)  
            except BadHeaderError:
                return JsonResponse(
                    {"send_mail_failed": "Invalid header found or Send Email Failed"}
                )
            return JsonResponse({"send_mail_successfully": "successfully"})
        return JsonResponse({"error": form.errors if form.errors else None})


@method_decorator(login_required, name="dispatch")
class ChangePasswordView(PasswordChangeView):
    template_name = "registration/change_password.html"
    form_class = PasswordChangeForm

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, data=self.request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return JsonResponse({"password_change_status": "success"})
        return JsonResponse({"error": form.errors if form.errors else None})


@method_decorator(login_required, name="dispatch")
class UserRequestListView(ListView):
    model = CustomUser
    template_name = "users_requests.html"
    success_url = reverse_lazy("users_auth:users-requests")
    ordering = ["-id"]
    queryset = CustomUser.objects.all()

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset_list = []
        if user.is_role_admin:
            # role admin 
            admin_queryset = list(queryset.filter(~Q(email=self.request.user.email), college_name = user.college_name, role = CustomUser.Role.ADMIN.value, is_verified = False))
            queryset_list.append({"admin" : admin_queryset})
            # role superuser
            superuser_queryset = list(queryset.filter(~Q(email=self.request.user.email), college_name = user.college_name, role = CustomUser.Role.SUPERUSER.value, is_verified = False))
            queryset_list.append({"superuser" : superuser_queryset})
            # role user
            user_queryset = list(queryset.filter(~Q(email=self.request.user.email), college_name = user.college_name, role=CustomUser.Role.USER.value, is_verified = False))
            queryset_list.append({"user" : user_queryset})
        if user.is_role_superuser:
            superuser_queryset = list(queryset.filter(~Q(email=self.request.user.email), college_name = user.college_name,role = CustomUser.Role.SUPERUSER.value, department__department_name = user.department.department_name, is_verified = False ))
            queryset_list.append({"superuser" : superuser_queryset})
        print(queryset_list)
        return queryset_list
    
    def batch_requests_verify(request, **kwargs):        
        batch =request.GET.get("batch", None)
        batch_id = (
            batch.split(",")
            if "," in batch
            else [
                batch,
            ]
        )
        updated_users=CustomUser.objects.filter(id__in=batch_id).update(is_verified = True,verified_by=request.user.username)
        associated_users = CustomUser.objects.filter(id__in=batch_id)
        if associated_users.exists():
            for user in associated_users:
                subject = "Welcome To TrackAlumni! Verification Done."
                email_template_name = "verify.html"
                c = {
                    "email": user.email,
                    "domain": get_current_site(request).domain,
                    "protocol": "http",
                }
                text = render_to_string(email_template_name, c)
                try:
                    send_mail(
                        subject=subject,
                        message = None,
                        from_email=DEFAULT_FROM_EMAIL,
                        recipient_list=[user.email],
                        fail_silently=False,
                        html_message=text   
                    )
                except BadHeaderError:
                    return HttpResponse("Invalid header found or Send Email Failed")
        return HttpResponseRedirect("/users_auth/requests/") 


@method_decorator(login_required, name="dispatch")
class UserListView(ListView):
    model = CustomUser
    template_name = "users.html"
    success_url = reverse_lazy("users_auth:user-list")
    ordering = ["-id"]
    queryset = CustomUser.objects.all()

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super().get_context_data(
            **kwargs,
            roles=list(CustomUser.Role.labels),
        )
        admin_count = len(list(CustomUser.objects.filter(~Q(email=self.request.user.email), college_name = user.college_name, role = CustomUser.Role.ADMIN.value, is_verified = True)))
        superuser_count = len(list(CustomUser.objects.filter(~Q(email=self.request.user.email), college_name = user.college_name, role = CustomUser.Role.SUPERUSER.value, is_verified = True)))
        user_count = len(list(CustomUser.objects.filter(~Q(email=self.request.user.email), college_name = user.college_name, role=CustomUser.Role.USER.value, is_verified = True)))
        context["admin_count"]=admin_count
        context["superuser_count"]=superuser_count
        context["user_count"]=user_count

        return context

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        queryset_list = []
        if user.is_role_admin:
            # role admin 
            admin_queryset = list(queryset.filter(~Q(email=self.request.user.email), college_name = user.college_name, role = CustomUser.Role.ADMIN.value, is_verified = True))
            queryset_list.append({"admin" : admin_queryset})
            # role superuser
            superuser_queryset = list(queryset.filter(~Q(email=self.request.user.email), college_name = user.college_name, role = CustomUser.Role.SUPERUSER.value, is_verified = True))
            queryset_list.append({"superuser" : superuser_queryset})
            # role user
            user_queryset = list(queryset.filter(~Q(email=self.request.user.email), college_name = user.college_name, role=CustomUser.Role.USER.value, is_verified = True))
            queryset_list.append({"user" : user_queryset})
        if user.is_role_superuser:
            superuser_queryset = list(queryset.filter(~Q(email=self.request.user.email), college_name = user.college_name,role = CustomUser.Role.SUPERUSER.value, department__department_name = user.department.department_name, is_verified = True ))
            queryset_list.append({"superuser" : superuser_queryset})
        return queryset_list

    def unverify_user(self, **kwargs):
        id = kwargs.get("pk")
        user = get_object_or_404(CustomUser, id=id)
        user.is_verified =False
        user.save()
        return redirect(reverse_lazy("users_auth:user-list"))

@method_decorator(login_required, name="dispatch")
class UserProfileView(UpdateView):
    form_class = UserUpdateForm
    template_name = "user_profile.html"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        college_obj = self.get_object().college_name
        context["designation_list"] = [model_to_dict(designation, fields=['id','designation']) for designation in list(college_obj.designation_List.all())]
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(
            instance=self.request.user, data=self.request.POST, files=self.request.FILES
        )
        if form.is_valid():
            form.save()
            return JsonResponse({"user_profile_status": "success"})
        return JsonResponse({"error": form.errors if form.errors else None})


class CreateUserView(CreateView):
    model = CustomUser
    form_class = UserCreateForm
    template_name = "singup.html"
    

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs, college_list= list(College.objects.all().values()),
                                                     role_list=list(CustomUser.Role.values))
        
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        form = self.form_class(data, self.request.FILES)
        if form.is_valid():
            user = form.save()
            subject_content = "Welcome To TrackAlumni! Set Your Password"
            mail_template= "password_set_email.html"
            send_invitation(self, self.request, user.email, subject_content,mail_template)
            user.is_active = False
            self.request.session['new_user'] = user.email
            self.request.session['new_user_role'] = user.role
            self.request.session['new_user_verified'] = user.is_verified
            self.request.session.save()
            return HttpResponseRedirect(reverse_lazy("college-registration:password-sent-to-admin"))
        return JsonResponse({"error": form.errors if form.errors else None})


@method_decorator(login_required, name="dispatch")
class DeleteUserView( DeleteView):
    model = CustomUser
    template_name = "user_delete.html"
    success_url = reverse_lazy("users_auth:users-requests")
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        super(DeleteUserView, self).post(request, *args, **kwargs)
        return JsonResponse({"delete_user_status": "success"})


@method_decorator(login_required, name="dispatch")
class ResendInvitationView(RedirectView):
    def get_redirect_url(self, pk, *args, **kwargs):
        user = CustomUser.objects.get(pk=pk)
        user.is_active = True
        user.save()
        send_invitation(self, user)
        user.is_active = False
        user.save()
        redirect_url = self.request.build_absolute_uri(
            reverse("users_auth:user-list", args=args)
        )
        return redirect_url

