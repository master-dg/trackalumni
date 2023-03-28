# Generated by Django 4.1.4 on 2023-02-16 16:56

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('users_auth', '0006_customuser_date_joined'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_no',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=10, null=True, unique=True),
        ),
    ]