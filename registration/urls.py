from django.contrib import admin
from django.urls import path
from .views import CollegeAdminRegistrationView,CollegeDatabaseView,dbload,CollegeDeptDesg,PasswordSentToAdmin,ResendMail,ChangeMail

app_name='college-registration'
urlpatterns = [
    path("",CollegeAdminRegistrationView.as_view(),name='college-admin-reg'),
    path("college-database/",CollegeDatabaseView.as_view(),name='college-database-create'),
    path("college-dept-desg/",CollegeDeptDesg.as_view(),name='college-dept-desg'),
    path("college-database-load/",dbload,name='college-database-load'),
    path("password-sent-to-admin/",PasswordSentToAdmin.as_view(),name='password-sent-to-admin'),
    path("password-resent-to-admin/",ResendMail.as_view(),name='password-resent-to-admin'),
    path("mail-change-of-admin/",ChangeMail.as_view(),name='mail-change-of-admin'),
   
      
]

