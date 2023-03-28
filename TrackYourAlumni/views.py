from django.views.generic import TemplateView
from registration.database_functions import db_load

class WelcomeTrackAlumniView(TemplateView):
    template_name="welcome.html"
    

class AboutDetailView(TemplateView):
    template_name="about.html"
   
class ContactDetailView(TemplateView):
    db_load()
    template_name="contact.html"
