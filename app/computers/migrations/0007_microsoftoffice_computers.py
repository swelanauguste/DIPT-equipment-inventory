# Generated by Django 5.1.3 on 2024-11-28 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computers', '0006_alter_microsoftoffice_product_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='microsoftoffice',
            name='computers',
            field=models.ManyToManyField(blank=True, related_name='office_computers', to='computers.computer'),
        ),
    ]