# Generated by Django 4.1.4 on 2023-01-28 20:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('departments', '0002_rename_designation_list_college_designation_list'),
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='database_info',
            options={'managed': True, 'verbose_name': 'Database_Info', 'verbose_name_plural': 'Database_Infos'},
        ),
        migrations.RenameField(
            model_name='database_info',
            old_name='name',
            new_name='db_name',
        ),
        migrations.AddField(
            model_name='database_info',
            name='db_creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='database_info',
            name='db_host',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='database_info',
            name='db_password',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='database_info',
            name='db_port',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AddField(
            model_name='database_info',
            name='db_user',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='database_info',
            name='collage_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='departments.college'),
        ),
        migrations.AlterUniqueTogether(
            name='database_info',
            unique_together={('db_creator', 'collage_name')},
        ),
        migrations.AlterModelTable(
            name='database_info',
            table='Database_Info',
        ),
        migrations.RemoveField(
            model_name='database_info',
            name='email',
        ),
        migrations.RemoveField(
            model_name='database_info',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='database_info',
            name='host',
        ),
        migrations.RemoveField(
            model_name='database_info',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='database_info',
            name='password',
        ),
        migrations.RemoveField(
            model_name='database_info',
            name='phone_no',
        ),
        migrations.RemoveField(
            model_name='database_info',
            name='port',
        ),
        migrations.RemoveField(
            model_name='database_info',
            name='user',
        ),
    ]