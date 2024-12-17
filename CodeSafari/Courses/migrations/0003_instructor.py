# Generated by Django 5.1.4 on 2024-12-17 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Courses', '0002_chapter_slug_course_slug_note_slug_section_slug_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('experience', models.IntegerField(default=0, help_text='Years of teaching experience')),
                ('profile_picture', models.ImageField(blank=True, null=True, upload_to='instructors/')),
                ('courses', models.ManyToManyField(blank=True, related_name='instructors', to='Courses.course')),
            ],
            options={
                'verbose_name': 'Instructor',
                'verbose_name_plural': 'Instructors',
            },
        ),
    ]
