# Generated by Django 5.1.3 on 2024-11-18 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('computers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computermodel',
            name='processor',
            field=models.CharField(blank=True, help_text='In GHz(e.g.:i5 2.9 GHz)', max_length=50, null=True),
        ),
    ]
