# from rest_framework import serializers
# from .models import BasicInformation,Skills,CollegeDetails

# class AllInformationSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = BasicInformation,CollegeDetails,Skills  
#         fields = ('PublicId', 'FirstName', 'LastName', 'Address', 'Country', 'Field')

# class CollegeDetailsSerializer(serializers.ModelSerializer):


#     class Meta:
#         model = CollegeDetails
#         fields = ('PublicId','CollegeName','DegreeName','StartYear','Endyear')


# class SkillsSerializer(serializers.ModelSerializer):


#     class Meta:
#         model = Skills
#         fields = ('PublicId','SkillName')