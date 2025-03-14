# Generated by Django 5.1.3 on 2024-11-28 19:51

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Computer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_project', models.BooleanField(default=False)),
                ('serial_number', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('warranty_info', models.CharField(blank=True, default='N/A', max_length=100, null=True, verbose_name='Warranty')),
                ('computer_name', models.CharField(blank=True, default='MCWT', max_length=100, null=True)),
                ('date_received', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('date_installed', models.DateField(blank=True, null=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='system_audit/')),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='ComputerModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('computer_type', models.CharField(choices=[('desktop', 'Desktop'), ('laptop', 'Laptop'), ('tablet', 'Tablet'), ('server', 'Server'), ('other', 'Other')], default='desktop', max_length=10)),
                ('processor', models.CharField(blank=True, help_text='In GHz(e.g.:i5 2.9 GHz)', max_length=100, null=True)),
                ('ram', models.CharField(blank=True, help_text='GB', max_length=5, null=True, verbose_name='RAM')),
                ('hdd', models.CharField(help_text='GB/TB', max_length=5, verbose_name='HDD/Storage')),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Maker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='MicrosoftOffice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_key', models.CharField(max_length=30, unique=True)),
                ('date_installed', models.DateField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('is_installed', models.BooleanField(default=False)),
                ('has_failed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='MicrosoftOfficeInstalled',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_installed', models.DateField(blank=True, null=True)),
                ('comments', models.TextField(blank=True, null=True)),
                ('has_failed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='MicrosoftOfficeVersion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(blank=True, max_length=100, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('date_received', models.DateField(blank=True, default=django.utils.timezone.now, null=True)),
                ('date_installed', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['model__name'],
            },
        ),
        migrations.CreateModel(
            name='MonitorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('image', models.FileField(blank=True, null=True, upload_to='monitor_models/')),
                ('notes', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='OperatingSystem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('colour', models.CharField(blank=True, max_length=10, null=True)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Statuses',
                'ordering': ['name'],
            },
        ),
    ]
