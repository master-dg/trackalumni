# Generated by Django 4.1.4 on 2023-02-12 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_alter_database_info_db_name'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='database_info',
            unique_together={('college_name',)},
        ),
    ]
