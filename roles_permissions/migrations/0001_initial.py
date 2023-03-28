# Generated by Django 4.1.4 on 2023-01-15 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission_name', models.CharField(choices=[(1, 'Gave Permssion To SuperUser'), (2, 'Gave Permmison To User'), (3, 'Search Data From DataBase'), (4, 'Analyze Data'), (5, 'Download Data File')], default=3, max_length=2)),
            ],
            options={
                'verbose_name': 'Permission',
                'verbose_name_plural': 'Permissions',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(choices=[('admin', 'Admin'), ('superuser', 'SuperUser'), ('user', 'User'), ('end_user', 'EndUser')], default='user', max_length=10)),
                ('permissions', models.ManyToManyField(to='roles_permissions.permission')),
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
            },
        ),
    ]