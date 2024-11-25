# Generated by Django 5.1.3 on 2024-11-19 17:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computers', '0006_operatingsystem_status_alter_computermodel_ram_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computer',
            name='os',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='computer_operating_systems', to='computers.operatingsystem', verbose_name='operating system'),
        ),
        migrations.AlterField(
            model_name='computermodel',
            name='ram',
            field=models.CharField(blank=True, help_text='GB', max_length=5, null=True, verbose_name='RAM'),
        ),
    ]
