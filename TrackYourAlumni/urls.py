"""TrackYourAlumni URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, reverse_lazy
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView, LogoutView, PasswordResetDoneView
from .views import WelcomeTrackAlumniView,ContactDetailView,AboutDetailView
from users_auth.views import LoginView, ResetPasswordView, ResendInvitationView, UserProfileView, ChangePasswordView
from users_auth.forms import SetPasswordForm

app_name='home'
urlpatterns = [
    path("",WelcomeTrackAlumniView.as_view(), name="welcome-trackalumni"),
    path("about/",AboutDetailView.as_view(), name="about"),
    path("contact/",ContactDetailView.as_view(), name="contact"),

    
    path("admin/", admin.site.urls),
    path('urlsearch/',include("UrlSearch.urls")),
    path('dashboard/',include(("dashboard.urls",'dashboard'),namespace='dashboard')),

    path("college-registration/",include(('registration.urls','college-registration'),namespace='college-registration')),
    path("users_auth/",include(('users_auth.urls','users_auth'),namespace='users_auth')),


    
    path("accounts/login/",LoginView.as_view(), name="login"),
    path("accounts/logout/",LogoutView.as_view(), name="logout"),
    path(
        "accounts/password-reset/",
        ResetPasswordView.as_view(),
        name="password-reset",
    ),
    path(
        "accounts/password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="registration/password_reset.html",
        ),
        name="password-reset-mail-done",
    ),
    path(
        "accounts/password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            form_class=SetPasswordForm,
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("password-reset-complete"),
        ),
        name="password-reset-confirm",
    ),
    path(
        "accounts/password-reset-complete/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password-reset-complete",
    ),
    path(
        "accounts/password-set-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            form_class=SetPasswordForm,
            template_name="registration/password_set_confirm.html",
            success_url=reverse_lazy("password-set-complete"),
        ),
        name="password-set-confirm",
    ),
    path(
        "accounts/password-set-complete/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_set_complete.html"
        ),
        name="password-set-complete",
    ),
    path("accounts/profile/", UserProfileView.as_view(), name="user-profile"),
    path(
        "accounts/change-password/",
        ChangePasswordView.as_view(),
        name="user-change-password",
    ),
    path(
        "users/resend-invitation/<int:pk>/",
        ResendInvitationView.as_view(),
        name="resend-invitation",
    ),
]
urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)

