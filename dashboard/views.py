
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from UrlSearch.models import BasicInformation,Skills, CollegeDetails,CompanyDetails
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from datetime import datetime
from datetime import timedelta
from chartjs.views.lines import BaseLineChartView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, UpdateView, DeleteView

# Create your views here.
def get_query_params(request):
    from_date = request.GET.get("fromdate", None)
    to_date = request.GET.get("todate", None)
    if from_date:
        from_date = datetime.strptime(from_date, "%Y-%m-%d")
    if to_date:
        to_date = datetime.strptime(to_date, "%Y-%m-%d")

    if not from_date and not to_date:
        today_date = timezone.now()
        from_date = today_date.replace(day=1)
        to_date = last_day_of_month(today_date)
    elif not from_date and to_date:
        from_date = to_date.replace(day=1)
    elif not to_date and from_date:
        to_date = last_day_of_month(from_date)

    sel_field_name = request.GET.getlist("field_name",None)
    sel_college = request.GET.getlist("college_name",None)
    sel_company=request.GET.getlist("company_name",None)
    sel_country = request.GET.getlist("country",None)
    sel_skills = request.GET.getlist("skills",None)
    sel_years = request.GET.getlist("years",None)
    return (from_date, to_date,sel_field_name, sel_college ,sel_company ,sel_country , sel_skills, sel_years)
    


def last_day_of_month(any_day):
    # this will never fail
    # get close to the end of the month for any day, and add 4 days 'over'
    next_month = any_day.replace(day=28) + timedelta(days=4)
    # subtract the number of remaining 'overage' days to get last day of current month, or said programattically said, the previous day of the first of next month
    return next_month - timedelta(days=next_month.day)

class BasicInfoListView(ListView):
    model = BasicInformation
    queryset = BasicInformation.objects.all()
    template_name = "data.html"
    success_url = reverse_lazy("dashboard:basic-info-list")

    def get_context_data(self, **kwargs):
        (from_date, to_date,sel_field_name, sel_college ,sel_company ,sel_country , sel_skills, sel_years)  = get_query_params(self.request)
        DB = self.request.user.college_name.college_name

        fields=BasicInformation.objects.using(DB).all().values_list('Field',flat=True).distinct()
        college_list = CollegeDetails.objects.using(DB).all().values_list('CollegeName',flat=True).distinct()
        country_list = BasicInformation.objects.using(DB).all().values_list('Country',flat=True).distinct()
        skill_list = Skills.objects.using(DB).all().values_list('SkillName',flat=True).distinct()
        batch_years = BasicInformation.objects.using(DB).all().values_list('batch_year',flat=True).distinct()
        company_list=CompanyDetails.objects.using(DB).all().values_list('CompanyName',flat=True).distinct()
        context=super().get_context_data(**kwargs,fields =fields,college_list = college_list, company_list=company_list,country_list = country_list, skill_list = skill_list,batch_years = batch_years, sel_field_name= sel_field_name , sel_college=sel_college,sel_company=sel_company, sel_country = sel_country, sel_skills = sel_skills, sel_years = sel_years, from_date=from_date, to_date=to_date, days=list(range(15,500,15)) )
        return context

    def get_queryset(self):
        (from_date, to_date,sel_field_name, sel_college ,sel_company ,sel_country , sel_skills, sel_years)  = get_query_params(self.request)
        DB = self.request.user.college_name.college_name
        queryset = BasicInformation.objects.using(DB).all()
        if from_date or to_date:
            queryset = queryset.filter(created_at__date__range=[from_date,to_date])
        if sel_field_name :
            queryset = queryset.filter(Field__in = sel_field_name)
        if sel_college :
            public_list = list(CollegeDetails.objects.using(DB).filter(CollegeName__in = sel_college).values_list("PublicId__id", flat=True))
            queryset = queryset.filter(id__in = public_list)
        if sel_company :
            public_list = list(CompanyDetails.objects.using(DB).filter(CompanyName__in = sel_company).values_list("PublicId__id", flat=True))
            queryset = queryset.filter(id__in = public_list)
        if sel_country:
            queryset = queryset.filter(Country__in = sel_country)
        if sel_skills:
            public_list = list(Skills.objects.using(DB).filter(SkillName__in = sel_skills).values_list("PublicId__id", flat=True))
            queryset = queryset.filter(id__in = public_list)
        if sel_years:
            queryset = queryset.filter(batch_year__in = sel_years)
        return queryset
    

    def add_scheduler_to_student(request):
        batch =request.GET.get("batch", None)
        batch_id = (
            batch.split(",")
            if "," in batch
            else [
                batch,
            ]
        )
        from UrlSearch.views import CreateScheduleTask
        from django_celery_beat.models import PeriodicTask
        from django.contrib import messages
        day=request.POST.get('day')
        description=request.POST.get('description')
        user_college_name = request.user.college_name.college_name

        temp_task_name = str(request.POST.get("task_name")+"_"+user_college_name)
        task_name=task_name=temp_task_name.lower().replace(' ','_')
        obj=PeriodicTask.objects.filter(name=task_name).first()
        if obj:
            messages.error(
                        request,
                        f"This Schedular aready applied",
                    )
            return redirect(
                        reverse_lazy("dashboard:basic-info-list")
                    )   
        length=CreateScheduleTask(task_name,description, None,None, request.user.email, user_college_name, day, batch_id )
        print(length,"----",batch_id)
        if length==0:
                messages.error(
                        request,
                        f"You have selected 0 urls",
                    )
                return redirect(
                        reverse_lazy("dashboard:basic-info-list")
                    )  
        else: 
            return redirect(
                    reverse_lazy("dashboard:basic-info-list")
            )  

    

@method_decorator(login_required, name="dispatch")
class UpdateStudentView(UpdateView):
    model = BasicInformation
    template_name = "data.html"
    fields = ['department','batch_year','college_id']
    success_url = reverse_lazy("dashboard:basic-info-list")

    def get_object(self, *args, **kwargs):
        PublicId = self.request.path.split("/")[4]
        obj = BasicInformation.objects.using(self.request.user.college_name.college_name).filter(PublicId = PublicId).first()
        return obj  


@method_decorator(login_required, name="dispatch")
class DeleteStudentView(DeleteView):
    model = BasicInformation
    template_name = "data.html"
    success_url = reverse_lazy("dashboard:basic-info-list")

    def get_object(self, *args, **kwargs):
        PublicId = self.request.path.split("/")[4]
        obj = BasicInformation.objects.using(self.request.user.college_name.college_name).filter(PublicId = PublicId).first()
        return obj 
    

    def bulk_delete_student(request, **kwargs):        
        batch =request.GET.get("batch", None)
        batch_id = (
            batch.split(",")
            if "," in batch
            else [
                batch,
            ]
        )
        deleted_students=BasicInformation.objects.using(request.user.college_name.college_name).filter(PublicId__in=batch_id).delete()
        # associated_users = CustomUser.objects.filter(id__in=batch_id)
        return HttpResponseRedirect("/dashboard/student-records/") 
    


@method_decorator(login_required, name="dispatch")
class AnalyticsView(TemplateView):
    template_name = "analytics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        (
            sel_field_name, sel_college ,sel_company,sel_country , sel_skills, sel_year
        ) = get_chart_query_params(self.request)

        DB = self.request.user.college_name.college_name

        fields=BasicInformation.objects.using(DB).all().values_list('Field',flat=True).distinct()
        college_list = CollegeDetails.objects.using(DB).all().values_list('CollegeName',flat=True).distinct()
        company_list=CompanyDetails.objects.using(DB).all().values_list('CompanyName',flat=True).distinct()
        country_list = BasicInformation.objects.using(DB).all().values_list('Country',flat=True).distinct()
        skill_list = Skills.objects.using(DB).all().values_list('SkillName',flat=True).distinct()
        batch_years = BasicInformation.objects.using(DB).all().values_list('batch_year',flat=True).distinct()
        context=super().get_context_data(**kwargs,fields =fields,college_list = college_list,company_list=company_list, country_list = country_list, skill_list = skill_list,batch_years = batch_years, sel_field_name= sel_field_name , sel_college=sel_college, sel_country = sel_country, sel_skills = sel_skills, sel_year = sel_year)
        today_date = timezone.now()
        context["students_count"] = BasicInformation.objects.all().count()
        path = self.request.get_full_path()
        context["query_string"] = path.split("?")[-1] if "?" in path else ""
        return context


def get_chart_query_params(request):
    query_params = {}
    for key, value in request.GET.items():
        query_params[key.replace("amp;","")] = value
    sel_field_name = query_params.get("field_name", None)
    sel_college = query_params.get("college_name",None)
    sel_company = query_params.get("company_name",None)
    sel_country = query_params.get("country", None)
    sel_skills = query_params.get("skills", None)
    sel_year = query_params.get("year", None)
    return (sel_field_name, sel_college ,sel_company,sel_country , sel_skills, sel_year)


#x-axis: batch_years, y-axix: no of students
class BatchYearChartJSONView(BaseLineChartView):
    students = None
    batch_years_list = None
    DB = None

    def get_context_data(self, **kwargs):
        self.DB = self.request.user.college_name.college_name
        self.students = BasicInformation.objects.using(self.DB).all()
        return super().get_context_data(**kwargs)

    def get_labels(self):
        """Return years as labels for the x-axis."""
        starting_year = 2000
        current_year = datetime.today().year + 4
        self.batch_years_list = [year for year in range(starting_year, current_year+1)]
        return self.batch_years_list

    def get_providers(self):
        """Return names of datasets."""
        dataset_list = []
        (sel_field_name, sel_college ,sel_company,sel_country , sel_skills, sel_year ) = get_chart_query_params(self.request)
        if sel_field_name:
            dataset_list.append("Fields_students")
        if sel_college:
            dataset_list.append("Colleges_students")
        if sel_company:
            dataset_list.append("Company_students")
        if sel_country:
            dataset_list.append("Countries_students")
        if sel_skills:
            dataset_list.append("Skills_students")
        if not ((sel_field_name or sel_college) or (sel_country or sel_skills)):
            dataset_list.append("Students")
        return dataset_list

    def get_data(self):
        """Return datasets to plot."""
        data = []
        (sel_field_name, sel_college ,sel_company,sel_country , sel_skills, sel_year ) = get_chart_query_params(self.request)
        batch_years_list = self.batch_years_list
        DB = self.DB
        if sel_field_name:
            data.append([self.students.filter(Field=sel_field_name, batch_year = year).count() for year in batch_years_list])
        if sel_college:
            public_list = list(CollegeDetails.objects.using(DB).filter(CollegeName = sel_college).values_list("PublicId__id", flat=True))
            data.append([self.students.filter(id__in = public_list, batch_year = year).count() for year in batch_years_list])
        if sel_company:
            public_list = list(CompanyDetails.objects.using(DB).filter(CompanyName = sel_company).values_list("PublicId__id", flat=True))
            data.append([self.students.filter(id__in = public_list, batch_year = year).count() for year in batch_years_list])
        if sel_country:
            data.append([self.students.filter(Country=sel_country, batch_year = year).count() for year in batch_years_list])
        if sel_skills:
            public_list = list(Skills.objects.using(DB).filter(SkillName = sel_skills).values_list("PublicId__id", flat=True))
            data.append([self.students.filter(id__in = public_list, batch_year = year).count() for year in batch_years_list])
        if not ((sel_field_name or sel_college) or (sel_country or sel_skills)):
            data.append([self.students.filter(batch_year = year).count() for year in batch_years_list])
        return data
    
    def get_colors(self):
        return iter([(65,105,225),(255,105,180),(39,195,226),(180,65,225),(252, 177, 3)])


# class FieldPieChartView(HighChartPieView):
#     model = BasicInformation
#     fields = ['Field']
#     title = 'Field Distribution'

#     def get_labels(self):

#         return [obj.Field for obj in self.get_queryset()]

#     def get_data(self):
#         queryset = self.get_queryset()
#         print(queryset, "----queryset")
#         total = queryset.count()
#         data = []
#         for obj in queryset:
#             count = BasicInformation.objects.filter(Field=obj.Field).count()
#             percentage = count / total * 100
#             data.append(percentage)
#         return data

# Fields Pie Chart
def field_pie_chart(request):
    DB = request.user.college_name.college_name
    fields = BasicInformation.objects.using(DB).all().values_list('Field',flat=True).distinct()
    fields_names = [field for field in fields]
    fields_counts = [BasicInformation.objects.using(DB).filter(Field = field).count() for field in fields ]

    fields_dict = dict(zip(fields_names, fields_counts))
    data = {
        "fields_labels": fields_names,
        "fields_counts": fields_counts,
        "fields_dict": fields_dict,
    }
    response = JsonResponse(data)
    return response


# Batch Years Pie Chart
def batch_year_pie_chart(request):
    DB = request.user.college_name.college_name
    batch_years = BasicInformation.objects.using(DB).all().values_list('batch_year',flat=True).distinct()
    batch_years_names = [year for year in batch_years]
    batch_years_counts = [BasicInformation.objects.using(DB).filter(batch_year = year).count() for year in batch_years ]

    batch_years_dict = dict(zip(batch_years_names, batch_years_counts))
    data = {
        "batch_years_labels": batch_years_names,
        "batch_years_counts": batch_years_counts,
        "batch_years_dict": batch_years_dict,
    }
    response = JsonResponse(data)
    return response


# Countries Pie chart
def country_pie_chart(request):
    DB = request.user.college_name.college_name
    countries = BasicInformation.objects.using(DB).all().values_list('Country',flat=True).distinct()
    countries_names = [country for country in countries]
    countries_counts = [BasicInformation.objects.using(DB).filter( Country= country).count() for country in countries ]

    countries_dict = dict(zip(countries_names, countries_counts))
    data = {
        "countries_labels": countries_names,
        "countries_counts": countries_counts,
        "countries_dict": countries_dict,
    }
    response = JsonResponse(data)
    return response


# Skills Pie Chart
def skills_pie_chart(request):
    DB = request.user.college_name.college_name
    skills = Skills.objects.using(DB).all().values_list('SkillName',flat=True).distinct()
    skills_names = [skill for skill in skills]
    skills_counts = [Skills.objects.using(DB).filter(SkillName = skill).count() for skill in skills ]

    skills_dict = dict(zip(skills_names, skills_counts))
    data = {
        "skills_labels": skills_names,
        "skills_counts": skills_counts,
        "skills_dict": skills_dict,
    }
    response = JsonResponse(data)
    return response


def college_pie_chart(request):
    DB = request.user.college_name.college_name
    colleges = CollegeDetails.objects.using(DB).all().values_list('CollegeName',flat=True).distinct()
    colleges_names = [college for college in colleges]
    colleges_counts = [CollegeDetails.objects.using(DB).filter(CollegeName = college).count() for college in colleges ]

    colleges_dict = dict(zip(colleges_names, colleges_counts))
    data = {
        "colleges_labels": colleges_names,
        "colleges_counts": colleges_counts,
        "colleges_dict": colleges_dict,
    }
    response = JsonResponse(data)
    return response


def company_pie_chart(request):
    DB = request.user.college_name.college_name
    companys = CompanyDetails.objects.using(DB).all().values_list('CompanyName',flat=True).distinct()
    company_names = [company for company in companys]
    company_counts = [CompanyDetails.objects.using(DB).filter(CompanyName = company).count() for company in companys ]

    companys_dict = dict(zip(company_names, company_counts))
    data = {
        "company_labels": company_names,
        "company_counts": company_counts,
        "companys_dict": companys_dict,
    }
    response = JsonResponse(data)
    return response


# College Based HorizontalBar chart
def get_data_for_college_based_chart(
    request,DB
):
    (sel_field_name, sel_college ,sel_company,sel_country , sel_skills, sel_year ) = get_chart_query_params(request)
    college_names = list(CollegeDetails.objects.using(DB).all().values_list('CollegeName',flat=True).distinct())
    college_students_count = []
    for college in college_names:
        college_based_public_list = list(CollegeDetails.objects.using(DB).filter(CollegeName = college).values_list("PublicId__id", flat=True))
        print(college_based_public_list, "-----colle based public list", college)
        colleges_conditions = Q(id__in= college_based_public_list)

        if sel_field_name:
            print("---1", sel_field_name)
            colleges_conditions = colleges_conditions & Q(Field=sel_field_name)

        if sel_skills:
            public_list = list(Skills.objects.using(DB).filter(SkillName = sel_skills).values_list("PublicId__id", flat=True))
            colleges_conditions = colleges_conditions & Q(id__in=public_list)

        if sel_year:
            colleges_conditions = colleges_conditions & Q(batch_year = sel_year)

        queryset_count = BasicInformation.objects.using(DB).filter(colleges_conditions).count()
        college_students_count.append(queryset_count)
    return {
        "labels": college_names,
        "college_students_count": college_students_count,
        "sel_field_name": sel_field_name,
        "sel_skills": sel_skills,
        "sel_year": sel_year
    }


def college_based_chart(request):
    DB = request.user.college_name.college_name
    data = get_data_for_college_based_chart(request, DB)
    response = JsonResponse(data)
    return response


# Country Based HorizontalBar chart
def get_data_for_country_based_chart(
    request,DB
):
    (sel_field_name, sel_college ,sel_company,sel_country , sel_skills, sel_year ) = get_chart_query_params(request)
    country_names = list(BasicInformation.objects.using(DB).all().values_list('Country',flat=True).distinct())
    country_students_count = []
    
    for country in country_names:
        countries_conditions = Q(Country= country)

        if sel_field_name:
            countries_conditions = countries_conditions & Q(Field=sel_field_name)

        if sel_skills:
            public_list = list(Skills.objects.using(DB).filter(SkillName = sel_skills).values_list("PublicId__id", flat=True))
            countries_conditions = countries_conditions & Q(id__in=public_list)

        if sel_year:
            countries_conditions = countries_conditions & Q(batch_year = sel_year)

        country_students_count.append(BasicInformation.objects.filter(countries_conditions).count())
    return {
        "labels": country_names,
        "country_students_count": country_students_count,
        "sel_field_name": sel_field_name,
        "sel_skills": sel_skills,
        "sel_year": sel_year
    }


def country_based_chart(request):
    DB = request.user.college_name.college_name
    data = get_data_for_country_based_chart(request, DB)
    response = JsonResponse(data)
    return response
