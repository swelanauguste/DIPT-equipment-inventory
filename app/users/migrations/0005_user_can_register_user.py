# Generated by Django 5.1.3 on 2025-01-23 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_is_tech'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_register_user',
            field=models.BooleanField(default=False),
        ),
    ]
