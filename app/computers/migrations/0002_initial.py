# Generated by Django 5.1.3 on 2024-11-28 19:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('computers', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='computer',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='computer_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='computer',
            name='deleted_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='computer',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='computer_departments', to='users.department'),
        ),
        migrations.AddField(
            model_name='computer',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='computer_locations', to='users.location'),
        ),
        migrations.AddField(
            model_name='computer',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='computer_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='computer',
            name='user',
            field=models.ManyToManyField(blank=True, related_name='computer_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='computermodel',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='computer_model_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='computermodel',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='computer_model_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='computer',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='computers', to='computers.computermodel'),
        ),
        migrations.AddField(
            model_name='computermodel',
            name='maker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='computer_models', to='computers.maker'),
        ),
        migrations.AddField(
            model_name='microsoftoffice',
            name='computer',
            field=models.ForeignKey(blank=True, help_text='serial number', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='office_installations', to='computers.computer'),
        ),
        migrations.AddField(
            model_name='microsoftoffice',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ms_office_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='microsoftoffice',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ms_office_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='microsoftofficeinstalled',
            name='computer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='office_installed', to='computers.computer'),
        ),
        migrations.AddField(
            model_name='microsoftofficeinstalled',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='office_installed_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='microsoftofficeinstalled',
            name='microsoft_office',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='installed_office', to='computers.microsoftoffice'),
        ),
        migrations.AddField(
            model_name='microsoftofficeinstalled',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='office_installed_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='microsoftofficeversion',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='version_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='microsoftofficeversion',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='version_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='microsoftoffice',
            name='version',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='computers.microsoftofficeversion'),
        ),
        migrations.AddField(
            model_name='monitor',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='monitor_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='monitor',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='monitor_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='computer',
            name='monitor',
            field=models.ManyToManyField(blank=True, related_name='monitors', to='computers.monitor'),
        ),
        migrations.AddField(
            model_name='monitormodel',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monitor_model_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='monitormodel',
            name='maker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='monitor_models', to='computers.maker'),
        ),
        migrations.AddField(
            model_name='monitormodel',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='monitor_model_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='monitor',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='monitors', to='computers.monitormodel'),
        ),
        migrations.AddField(
            model_name='computer',
            name='os',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='computer_operating_systems', to='computers.operatingsystem', verbose_name='operating system'),
        ),
        migrations.AddField(
            model_name='computer',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='computer_status', to='computers.status'),
        ),
    ]