# Generated by Django 5.1.4 on 2024-12-17 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0006_student'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_approved_instructor',
            field=models.BooleanField(default=False),
        ),
    ]