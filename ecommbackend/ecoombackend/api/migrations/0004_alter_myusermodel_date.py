# Generated by Django 5.1 on 2024-08-16 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_myusermodel_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myusermodel',
            name='date',
            field=models.DateField(auto_created=True, null=True),
        ),
    ]
