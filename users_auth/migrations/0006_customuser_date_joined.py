# Generated by Django 4.1.4 on 2023-02-13 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_auth', '0005_remove_customuser_date_joined_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='date_joined',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]