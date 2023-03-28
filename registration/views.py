# Create your views here.
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from .forms import CollegeAdminCreationForm, CollegeDataBaseCreateForm
from django.urls import reverse_lazy
from registration.models import Database_Info
from users_auth.models import CustomUser
from departments.models import College, Designation, Department
from .database_functions import create_db, db_load, db_migrate, db_store,delete_db
from django.http import JsonResponse
from registration.utils import send_invitation
from TrackYourAlumni.settings import DEFAULT_DATABASE_HOST,DEFAULT_DATABASE_PORT,DEFAULT_DATABASE_USERNAME,DEFAULT_DATABASE_PASSWORD


def dbload(request):
    return render(request, 'db_load.html')


class CollegeAdminRegistrationView(CreateView):
    model = CustomUser
    form_class = CollegeAdminCreationForm
    template_name = 'college_admin_reg.html'

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            admin_of_db = form.instance
            admin_of_db.is_superuser = True
            admin_of_db.is_role_admin = True
            admin_of_db.is_verified = True
            admin_of_db.role=CustomUser.Role.ADMIN.value
            admin_of_db.is_active = True
            admin_of_db.save()
            
            self.request.session['new_user'] = admin_of_db.email
            self.request.session['new_user_role'] = admin_of_db.role
            self.request.session['new_user_verified'] = admin_of_db.is_verified

            self.request.session.save()
            
            subject_content = "Welcome To TrackAlumni! Set Your Password"
            mail_template= "password_set_email.html"
            send_invitation(self, self.request, admin_of_db.email, subject_content,mail_template)
            
            return JsonResponse({"admin_reg_success": "success"})
        return JsonResponse({"error": form.errors if form.errors else None})


class CollegeDatabaseView(CreateView):
    model = Database_Info
    form_class = CollegeDataBaseCreateForm
    success_url = reverse_lazy("college-registration:college-dept-desg")
    template_name = 'college_db_reg.html'
    success_message = "You Craete Table in your Database"

    def post(self,  request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            college_db  = form.instance
            college_obj=College.objects.filter(college_name__iexact = college_db.college_name).first()
            if college_obj :
                return JsonResponse({"college_exist" : "This College is already exists. "})

            #it's check same user than change only 
            user_obj = CustomUser.objects.filter(email=self.request.session['new_user']).first()
            old_college_data=Database_Info.objects.filter(db_creator=user_obj).first()
            if old_college_data:
                print("deleted old colleg-",old_college_data)
                old_college_data.delete()
                if old_college_data.db_host=="localhost":
                    delete_db(old_college_data.db_name)
                return JsonResponse({"multi_db_error" : "You can't create multi databases. "})

            checkbox_value = self.request.POST.get('checkbox_choose')
            if (not checkbox_value):
                temp_name=self.request.POST.get('college_name').lower().replace(" ","_")
                db_name1 = temp_name
                db_create_status = create_db(db_name1)

                if db_create_status==1:
                    return JsonResponse({"db_create_error" : "Please try again or wait, working in progress" })
                college_db.db_name = db_name1
                college_db.db_user = DEFAULT_DATABASE_USERNAME
                college_db.db_port = DEFAULT_DATABASE_PORT
                college_db.db_password = DEFAULT_DATABASE_PASSWORD
                college_db.db_host = DEFAULT_DATABASE_HOST

            
            user_obj.role=CustomUser.Role.ADMIN
            user_obj.save()
            college_db.db_creator = user_obj
            form.save()
        
            status = db_store(temp=college_db)
            if status == 1 and checkbox_value:
                Database_Info.objects.filter(college_name=college_db.college_name).delete()
                if college_db.db_host==DEFAULT_DATABASE_HOST:
                    delete_db(college_db.db_name)

                super().form_invalid(form)
                return JsonResponse({"error" : form.errors if form.errors else None})

            self.request.session['college_name'] = college_db.college_name
            self.request.session.save()
            db_load()
            return JsonResponse({"db_create_success" : "success"})
        return JsonResponse({"error": form.errors if form.errors else None})    


class CollegeDeptDesg(TemplateView):
    template_name = "college_dept_desg.html"
    success_url = reverse_lazy("registration:college-database-load")

    def get_context_data(self, **kwargs):
        coll_name = self.request.session['college_name']
        context = super().get_context_data(**kwargs, dept_list=list(Department.objects.all().values()),
                                           desg_list=list(Designation.objects.all().values()),college_name=coll_name)
        return context

    def post(self, request, *args, **kwargs):

        dept_list = set(self.request.POST.getlist("department_list"))
        desg_list = set(self.request.POST.getlist("designation_list"))

        college_name = self.request.session['college_name']
        college_obj = College.objects.create(college_name=college_name)

        user_obj = CustomUser.objects.filter(email=self.request.session['new_user']).first()
        user_obj.college_name=college_obj
        user_obj.save()

        print(college_name, "---colloge name")
        print(dept_list, "---detment")
        print(desg_list, "---designation")

    
        for dept in dept_list:
            dept_obj = Department.objects.filter(department_name=dept).first()
            if dept_obj:
                print(dept, "-----Exits dept")
                college_obj.department_List.add(dept_obj)
            else:
                print(dept, "--not dept Exits")
                dept_temp = Department.objects.create(department_name=dept)
                college_obj.department_List.add(dept_temp)

        for desg in desg_list:
            desg_obj = Designation.objects.filter(designation=desg).first()
            if desg_obj:
                print(desg, "-----Exits desg")
                college_obj.designation_List.add(desg_obj)
            else:
                print(desg, "--not Exits desg")
                desg_temp = Designation.objects.create(designation=desg)
                college_obj.designation_List.add(desg_temp)
        return render(request, "db_load.html")



class PasswordSentToAdmin(TemplateView):
    template_name = "password_sent.html"
    success_url = reverse_lazy("college-registration:password-sent-to-admin")

    def get_context_data(self, **kwargs):
        email=self.request.session['new_user']
        context = super().get_context_data(**kwargs, email=email)
        return context

class ResendMail(TemplateView):
    template_name = "password_sent.html"
    success_url = reverse_lazy("college-registration:password-sent-to-admin")
    def get_context_data(self, **kwargs):
        email=self.request.session['new_user']
        context = super().get_context_data(**kwargs, email=email,message="Resend Mail")
        return context
    
    def dispatch(self, request, *args, **kwargs):
        email=self.request.session['new_user']
        print(email,"mail  ----")
        subject_content = "Welcome To TrackAlumni! Set Your Password"
        mail_template= "password_set_email.html"
        send_invitation(self, self.request,email, subject_content,mail_template)
        return super().dispatch(request, *args, **kwargs)


class ChangeMail(TemplateView):
    template_name = "mail_change.html"
    success_url = reverse_lazy("college-registration:password-sent-to-admin")
    def get_context_data(self, **kwargs):
        email=self.request.session['new_user']
        print(email)
        context = super().get_context_data(**kwargs, email=email)
        return context
    
    
    def post(self, request, *args, **kwargs):
        old_email=self.request.session['new_user']
        new_email=request.POST.get("email")
        print(old_email,"old   new",new_email)
        obj=CustomUser.objects.filter(email=new_email).first()
        if obj:
            return render(request,"mail_change.html",{"messages":"Alredy Exists This Email Addreass","email":old_email})

        user_obj=CustomUser.objects.filter(email=old_email).first()
        user_obj.email=new_email
        user_obj.save()

        subject_content = "Welcome To TrackAlumni! Set Your Password"
        mail_template= "password_set_email.html"
        send_invitation(self, self.request,new_email, subject_content,mail_template)

        self.request.session['new_user']=new_email
        self.request.session.save()

        return render(request,"password_sent.html",{"email":new_email})

        



    
    

    