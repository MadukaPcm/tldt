# Generated by Django 3.2.20 on 2023-08-01 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tldetection', '0002_alter_user_profileimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='PCMUserPermissions',
            fields=[
                ('permission_unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('permission_name', models.CharField(default='', max_length=1600)),
                ('permission_code', models.CharField(default='', max_length=1600)),
                ('permission_createddate', models.DateField(auto_now_add=True)),
                ('permission_createdby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_permission_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Permissions',
                'db_table': 'tsms_user_permissions',
                'ordering': ['-permission_createddate'],
            },
        ),
        migrations.CreateModel(
            name='PCMUserRoles',
            fields=[
                ('role_unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('role_name', models.CharField(default='', max_length=1600)),
                ('role_description', models.CharField(default='', max_length=1600)),
                ('role_createddate', models.DateField(auto_now_add=True)),
                ('role_createdby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_role_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Roles',
                'db_table': 'tsms_user_roles',
                'ordering': ['-role_createddate'],
            },
        ),
        migrations.CreateModel(
            name='PCMUsersWithRoles',
            fields=[
                ('user_with_role_unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('user_with_role_createddate', models.DateField(auto_now_add=True)),
                ('user_with_role_createdby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_with_role_creator', to=settings.AUTH_USER_MODEL)),
                ('user_with_role_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_role_name', to='tldetection.pcmuserroles')),
                ('user_with_role_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Users with Roles',
                'db_table': 'tsms_user_with_roles',
                'ordering': ['-user_with_role_createddate'],
            },
        ),
        migrations.CreateModel(
            name='PCMUsersWithPermissions',
            fields=[
                ('user_with_permission_unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('user_with_permission_createddate', models.DateField(auto_now_add=True)),
                ('user_with_permission_createdby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_with_permission_creator', to=settings.AUTH_USER_MODEL)),
                ('user_with_permission_permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_permission_name', to='tldetection.pcmuserpermissions')),
                ('user_with_permission_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permission_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Users with Permissions',
                'db_table': 'tsms_user_with_permissions',
                'ordering': ['-user_with_permission_createddate'],
            },
        ),
        migrations.CreateModel(
            name='PCMUserRolesWithPermissions',
            fields=[
                ('role_with_permission_unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('permission_read_only', models.BooleanField(default=True)),
                ('role_with_permission_createddate', models.DateField(auto_now_add=True)),
                ('role_with_permission_createdby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_role_with_permission_creator', to=settings.AUTH_USER_MODEL)),
                ('role_with_permission_permission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_role_with_permission_permission', to='tldetection.pcmuserpermissions')),
                ('role_with_permission_role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_role_with_permission_role', to='tldetection.pcmuserroles')),
            ],
            options={
                'verbose_name_plural': 'Roles with Permissions',
                'db_table': 'dtp_user_role_with_permissions',
                'ordering': ['-role_with_permission_createddate'],
            },
        ),
        migrations.CreateModel(
            name='PCMUserPermissionsGroup',
            fields=[
                ('permission_group_unique_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('permission_group_name', models.CharField(default='', max_length=1600)),
                ('permission_group_description', models.CharField(default='', max_length=600, null=True)),
                ('permission_group_createddate', models.DateField(auto_now_add=True)),
                ('permission_group_createdby', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permission_group_creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Permission Groups',
                'db_table': 'tsms_user_permissions_group',
                'ordering': ['-permission_group_createddate'],
            },
        ),
        migrations.AddField(
            model_name='pcmuserpermissions',
            name='permission_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='permission_group', to='tldetection.pcmuserpermissionsgroup'),
        ),
    ]
