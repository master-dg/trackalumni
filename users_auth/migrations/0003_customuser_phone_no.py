# Generated by Django 4.1.4 on 2023-01-26 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_auth', '0002_alter_customuser_options_alter_customuser_managers_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='phone_no',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
