import pandas as pd
from linkedin_api import  Linkedin
from opencage.geocoder import OpenCageGeocode
from pprint import pprint
from UrlSearch.models import BasicInformation,CollegeDetails,Skills,CompanyDetails
from TrackYourAlumni.settings import GEO_KEY
user_list = []

#college or company location api
key =GEO_KEY
geocoder = OpenCageGeocode(key)

def location(name_key):
    results = geocoder.geocode(name_key)
    if len(results)==0: 
          city,country,state,continent = "NOT AVIALABLE" 
    else:
        try:
            city_key=[0,'components','city']
            country_key=[0,'components','country']
            state_key=[0,'components','country']
            continent_key=[0,'components','continent']
            city = get(results,city_key)
            country=get(results,country_key)
            state=get(results,state_key)
            continent= get(results,continent_key)
        except:
            city,country,state,continent = "NOT AVIALABLE","NOT AVIALABLE","NOT AVIALABLE","NOT AVIALABLE"
    return city,country,state,continent

#call LinkedIn server

def getapi(email,password):
    api=Linkedin(email,password)
    print("API-----",api)   
    return api

#default response from LInkedIn server
def getprofile(api,url):
    return  api.get_profile(url)

#extract public_id from linkedin url
def  extract_Publicid(line):
    line = line.strip()
    user_name = line.split('linkedin.com/in/')[1].split('\\')[0]
    return user_name

#differentiate keys from data
def get(d,l):
    try:
        if len(l)==1: return d[l[0]]
        return get(d[l[0]],l[1:])
    except:
        return "NOT AVIALABLE"

#get profile of people
def get_urlprofile(api,line):
            public_id=extract_Publicid(line)
            user_list.append(public_id)
            profile = api.get_profile(public_id)
            details=[]
            details.append(public_id)
            details.append(profile)
            return details


def get_update_profile(api,public_id):
    profile = api.get_profile(public_id)
    details=[]
    details.append(public_id)
    details.append(profile)
    return details
      
#get basic_info of people
def get_basicInformation(profile,public_id):
            lastName_key = ['lastName']
            address_key = ['address']
            locationName_key = ['locationName']
            firstName_key = ['firstName']
            fieldOfStudy_key = ['education', 0, 'fieldOfStudy']
        
            basic_information = {
                     "PublicId": public_id ,
                     "FirstName" : get(profile, firstName_key),
                     "LastName" : get(profile, lastName_key) ,
                     "Address" : get(profile, address_key),
                     "Country": get(profile, locationName_key),
                     "Field" : get(profile,fieldOfStudy_key),
                    }
            return basic_information

#get collegedetails of people
def get_collegedetails(profile,public_id):

            size = len(profile['education'])
            college_info=[]
            for i in range(0,size):
                degreeName_key = ['education', i, 'degreeName']
                schoolName_key = ['education', i,'schoolName']

                endYear_key = ['education', i, 'timePeriod', 'endDate', 'year']
                startYear_key = ['education', i, 'timePeriod', 'startDate', 'year']

                college_name=get(profile, schoolName_key)
                c_city,c_country,c_state,c_continent = location(college_name)

                college_details = {
                    "PublicId": public_id,
                    "CollegeName":college_name ,
                    "CollegeCity" : c_city,
                    "CollegeState" : c_state,
                    "CollegeCountry" : c_country,
                    "CollegeContient" : c_continent,
                    "DegreeName" : get(profile, degreeName_key),
                    "StartYear" : str(get(profile, startYear_key)),
                    "EndYear" : str(get(profile, endYear_key))
                }
                college_info.append(college_details)
            return college_info


#make location string

#get companydetails of people
def get_companydetails(profile,public_id):

            size = len(profile['experience'])
            company_info=[]
            for i in range(0,size):
                companyName_key = ['experience', i, 'companyName']
                jobTitle_key = ['experience', i, 'title']
                companyLocation_key = ['experience', i, 'geoLocationName']
                endYear_key = ['experience', i, 'timePeriod', 'endDate', 'year']
                startYear_key = ['experience', i, 'timePeriod', 'startDate', 'year']
                company_name= get(profile, companyName_key)
                c_city,c_country,c_state,c_continent = location(company_name)
                

                company_details = {
                    "PublicId": public_id,
                    "CompanyName": company_name ,
                    "CompanyCity" : c_city,
                    "CompanyState" : c_state,
                    "CompanyCountry" : c_country,
                    "CompanyContinent" : c_continent,
                    "JobTitle": get(profile, jobTitle_key) ,
                    "StartYear" : str(get(profile, startYear_key)),
                    "EndYear" : str(get(profile, endYear_key)),
                }
                company_info.append(company_details)
            return company_info

#get skills of people
def get_skill(api,public_id):
    skill_data=api.get_profile_skills(public_id)
    print(skill_data, "\n")
    skill_list=[]
    for j in range(len(skill_data)):
        skill_key=[j,'name']
        skill_dic={
            "PublicId" :public_id,
            "SkillName" :get(skill_data,skill_key) 
        }
        skill_list.append(skill_dic)
    return skill_list

#for txt file type
def read_txt(file):
    publicid_list=[]
    for line in file.readlines():
        publicid_list.append(str(line,'utf-8'))
    return publicid_list


#insert basic information
def insert_BasicInformation(profile,public_id,DB):
    basic_information=get_basicInformation(profile,public_id)
    basic_info_obj=BasicInformation.objects.using(DB).filter(PublicId=public_id)
    obj = None
    
    if basic_info_obj.first():
        basic_info_obj.update(FirstName = basic_information['FirstName'], 
            LastName= basic_information['LastName'], 
            Address= basic_information['Address'],
            Country= basic_information['Country'],
            Field= basic_information['Field']
        )
        obj = basic_info_obj.first()
    else:   
        obj=BasicInformation.objects.using(DB).create(PublicId = basic_information['PublicId'],
                    FirstName = basic_information['FirstName'], 
                    LastName= basic_information['LastName'], 
                    Address= basic_information['Address'],
                    Country= basic_information['Country'],
                    Field= basic_information['Field']
                )
    return obj

#insert college details 
def insert_CollegeDetails(profile,public_id,obj,DB):
    college_info=get_collegedetails(profile,public_id)
    CollegeDetails.objects.using(DB).filter(PublicId=obj).delete()
    for  key,college_detail in enumerate(college_info):
                print(college_detail)
                CollegeDetails.objects.using(DB).create(PublicId=obj,CollegeName=get(college_detail,['CollegeName']),
                                                CollegeCity=get(college_detail,['CollegeCity']),
                                                CollegeState=get(college_detail,['CollegeState']),
                                                CollegeCountry=get(college_detail,['CollegeCountry']),
                                                CollegeContinent=get(college_detail,['CollegeContient']),
                                                DegreeName=get(college_detail,['DegreeName']),
                                                StartYear=get(college_detail,['StartYear']),
                                                EndYear=get(college_detail,['EndYear']))
#insert company details 
def insert_CompanyDetails(profile,public_id,obj,DB):
    company_info=get_companydetails(profile,public_id)
    CompanyDetails.objects.using(DB).filter(PublicId=obj).delete()
    print("------------------",company_info,"-------")
    for  key,company_detail in enumerate(company_info):
                CompanyDetails.objects.using(DB).create(PublicId=obj,CompanyName=get(company_detail,['CompanyName']),
                                                JobTitle=get(company_detail,['JobTitle']),
                                                c_StartYear=get(company_detail,['StartYear']),
                                                c_EndYear=get(company_detail,['EndYear']),
                                                CompanyCity=get(company_detail,['CompanyCity']),
                                                CompanyState=get(company_detail,['CompanyState']),
                                                CompanyCountry=get(company_detail,['CompanyCountry']),
                                                CompanyContinent=get(company_detail,['CompanyContinent']))
#insert skills 
def insert_Skills(api,public_id,obj,DB):
    skill_list=get_skill(api,public_id)
    Skills.objects.using(DB).filter(PublicId=obj).delete()
    for key,skills in enumerate(skill_list):
            Skills.objects.using(DB).create(PublicId=obj,SkillName=get(skills,['SkillName']))