# Generated by Django 5.1.3 on 2025-01-17 15:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0007_alter_notice_message_alter_notice_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notice',
            name='title',
            field=models.CharField(max_length=255, null=True),
        ),
    ]