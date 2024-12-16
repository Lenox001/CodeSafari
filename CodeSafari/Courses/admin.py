from django.contrib import admin
from .models import Course, Chapter, Section, Note

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'order')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'section')
