# Generated by Django 4.1.4 on 2022-12-21 11:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UrlSearch', '0004_alter_basicinformation_id_alter_collegedetails_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collegedetails',
            name='EndYear',
            field=models.IntegerField(max_length=15),
        ),
        migrations.AlterField(
            model_name='collegedetails',
            name='StartYear',
            field=models.CharField(max_length=15),
        ),
    ]
