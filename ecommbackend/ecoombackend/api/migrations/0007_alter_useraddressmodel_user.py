# Generated by Django 5.1 on 2024-09-21 11:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_myusermodel_alternate_phone_myusermodel_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraddressmodel',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='addresses', to='api.myusermodel'),
        ),
    ]
