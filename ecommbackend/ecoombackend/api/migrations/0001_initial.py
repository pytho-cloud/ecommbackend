# Generated by Django 5.0.7 on 2024-08-08 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImageModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
    ]
