# Generated by Django 5.1.3 on 2024-11-28 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computers', '0005_alter_microsoftoffice_product_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='microsoftoffice',
            name='product_key',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
