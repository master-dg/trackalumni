from django.contrib import admin
from django.urls import path,include
from UrlSearch.views import *
# from UrlSearch.databaseinput import get_prfile_data   
from .views import SearchPeopleFromUrl,SetScheduler,SetDeleteeScheduler, SetUpdateScheduler,trigger_task
app_name= "urlsearch"

urlpatterns = [
    path('search-people/',SearchPeopleFromUrl.as_view(),name='getProfile'),
    path('set-scheduler/',SetScheduler.as_view(),name='scheduler'),
    path('set-scheduler/edit-task/<int:pk>/',SetUpdateScheduler.as_view(),name='scheduler-edit'),
    path('set-scheduler/delete-task/<int:pk>/',SetDeleteeScheduler.as_view(),name='scheduler-delete'),
    path('set-scheduler/trigger-task/<int:pk>/',trigger_task,name='trigger-task'),
    # path('get/',get_prfile_data,name='getProfiledata'),
]