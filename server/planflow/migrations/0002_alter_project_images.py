# Generated by Django 4.2 on 2024-12-20 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planflow', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='images',
            field=models.ImageField(blank=True, null=True, upload_to='media/'),
        ),
    ]