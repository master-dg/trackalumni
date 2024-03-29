# Generated by Django 4.1.4 on 2023-01-28 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_auth', '0004_alter_customuser_phone_no'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='date_joined',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='date_profile_updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_role_user',
            field=models.BooleanField(default=False),
        ),
    ]
