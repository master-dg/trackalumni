# Generated by Django 4.1.4 on 2023-02-18 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0009_alter_database_info_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='database_info',
            name='db_user',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
