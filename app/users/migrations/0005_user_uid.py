# Generated by Django 5.1.3 on 2024-11-20 15:06

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
