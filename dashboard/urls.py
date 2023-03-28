from django.contrib import admin
from django.urls import path,include
from .views import BasicInfoListView, BatchYearChartJSONView, AnalyticsView,field_pie_chart, skills_pie_chart,country_pie_chart, batch_year_pie_chart,college_pie_chart,college_based_chart,country_based_chart,company_pie_chart
from .views import UpdateStudentView, DeleteStudentView

app_name= "dashboard"

urlpatterns = [
    path("analysis/", AnalyticsView.as_view(), name="index"),
    path('student-records/',BasicInfoListView.as_view(),name='basic-info-list'),
    path('student-records/update-student/<str:PublicId>/',UpdateStudentView.as_view(),name='update-student'),
    path('student-records/delete-student/<str:PublicId>/',DeleteStudentView.as_view(),name='delete-student'),
    path('student-records/bulk-delete-student/',DeleteStudentView.bulk_delete_student,name='bulk-delete-student'),
    path('student-records/add-scheduler/',BasicInfoListView.add_scheduler_to_student,name='add-scheduler-student'),

    path("field-pie-chart/", field_pie_chart, name="field-pie-chart"),
    path("batch-year-pie-chart/", batch_year_pie_chart, name="batch-year-pie-chart"),
    path("skills-pie-chart/", skills_pie_chart, name="skill-pie-chart"),
    path("country-pie-chart/",country_pie_chart, name="country-pie-chart"),
    path("company-pie-chart/",company_pie_chart, name="company-pie-chart"),
    path("college-pie-chart/",college_pie_chart, name="college-pie-chart"),

    path("batchyear-based-chart/", BatchYearChartJSONView.as_view(), name="batch-year-chart"),
    path("college-based-chart/", college_based_chart, name="college-based-chart"),
    # path("skills-based-chart/", SkillsChartJSONView.as_view(), name="skills-based-chart"),
    path("country-based-chart/", country_based_chart, name="country-based-chart"),
]