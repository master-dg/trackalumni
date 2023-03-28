# Generated by Django 4.1.4 on 2023-03-26 08:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('UrlSearch', '0019_alter_collegedetails_publicid_alter_skills_publicid'),
    ]

    operations = [
        migrations.AddField(
            model_name='collegedetails',
            name='CollegeCity',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='collegedetails',
            name='CollegeContinent',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='collegedetails',
            name='CollegeCountry',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='collegedetails',
            name='CollegeSate',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='collegedetails',
            name='DegreeName',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='collegedetails',
            name='EndYear',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='collegedetails',
            name='StartYear',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.CreateModel(
            name='CompanyDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CompanyName', models.CharField(max_length=100, null=True)),
                ('JobTitle', models.CharField(max_length=100, null=True)),
                ('c_StartYear', models.CharField(max_length=15, null=True)),
                ('c_EndYear', models.CharField(max_length=15, null=True)),
                ('c_Location', models.CharField(max_length=100, null=True)),
                ('PublicId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_company_details', to='UrlSearch.basicinformation')),
            ],
        ),
    ]