# Generated by Django 4.1.4 on 2023-03-26 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UrlSearch', '0022_rename_c_location_companydetails_companycity_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasksinfo',
            name='batch_year',
        ),
        migrations.RemoveField(
            model_name='tasksinfo',
            name='department',
        ),
        migrations.AddField(
            model_name='tasksinfo',
            name='task_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
