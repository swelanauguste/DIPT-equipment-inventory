# Generated by Django 5.1.3 on 2024-12-06 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0004_remove_ticket_ticket_category_ticket_ticket_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='ticket_category',
        ),
        migrations.AddField(
            model_name='ticket',
            name='ticket_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='tickets.ticketcategory', verbose_name='category'),
        ),
    ]