# Generated by Django 4.2 on 2024-12-20 15:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('priority', models.CharField(choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')], default='Medium', max_length=10)),
                ('category', models.CharField(max_length=255)),
                ('status', models.CharField(choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Not Started', max_length=20)),
                ('images', models.ImageField(blank=True, null=True, upload_to='projects/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
