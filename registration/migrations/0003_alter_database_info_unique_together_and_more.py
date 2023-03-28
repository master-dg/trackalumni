# Generated by Django 4.1.4 on 2023-02-12 15:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration', '0002_alter_database_info_options_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='database_info',
            unique_together={('db_creator',)},
        ),
        migrations.AddField(
            model_name='database_info',
            name='college_name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.RemoveField(
            model_name='database_info',
            name='collage_name',
        ),
    ]
