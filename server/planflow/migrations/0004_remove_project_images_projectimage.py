# Generated by Django 4.2 on 2024-12-20 15:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('planflow', '0003_alter_project_images'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='images',
        ),
        migrations.CreateModel(
            name='ProjectImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='projects-images/')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='planflow.project')),
            ],
        ),
    ]
