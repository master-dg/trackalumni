from django import template
from django.forms.models import model_to_dict
register = template.Library()


@register.filter("startswith")
def startswith(text, starts):
    return text.startswith(starts)


@register.filter("get_value")
def get_value(dictionary, key):
    return dictionary.get(key)


@register.filter("replace_commas")
def replace_commas(string):
    val = str(string)
    return val.replace(",", "")

@register.filter("display_dict")
def display_dict(object):
    dict = model_to_dict(object, fields=['CollegeName','DegreeName','StartYear','EndYear', 'CollegeCity','CollegeState','CollegeCountry','CollegeContinent'])
    return str(dict).replace("{","").replace("}","")

@register.filter("display_dict_company")
def display_dict(object):
    dict = model_to_dict(object, fields=['CompanyName','JobTitle', 'c_StartYear','c_EndYear','CompanyCity','CompanyState','CompanyCountry','CompanyContinent'])
    return str(dict).replace("{","").replace("}","")