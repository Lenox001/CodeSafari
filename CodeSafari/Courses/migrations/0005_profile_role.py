# Generated by Django 5.1.4 on 2024-12-17 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0004_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('student', 'Student'), ('instructor', 'Instructor')], default='student', max_length=20),
        ),
    ]
