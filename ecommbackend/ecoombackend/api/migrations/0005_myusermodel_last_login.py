# Generated by Django 5.1 on 2024-08-16 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_myusermodel_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='myusermodel',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
