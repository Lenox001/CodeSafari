from django.contrib import admin
from .models import Course, Chapter, Section, Note, Instructor, Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register Course model
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'updated_at')
    search_fields = ('title',)

# Register Chapter model
@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    search_fields = ('title',)
    list_filter = ('course',)

# Register Section model
@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'chapter', 'order')
    search_fields = ('title',)
    list_filter = ('chapter',)

# Register Note model
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'section')
    search_fields = ('title',)
    list_filter = ('section',)

# Register Instructor model
@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'experience']
    search_fields = ['first_name', 'last_name', 'email']

# Register Profile model
# admin.py
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_picture', 'is_approved_instructor')  # Include the approval flag
    search_fields = ('user__username', 'bio')
    list_filter = ('user__is_active', 'is_approved_instructor')  # Add filter by approval status

    # Allow admins to edit the approval status directly from the profile admin
    list_editable = ('is_approved_instructor',)


# Customize User model display (if needed)
class CustomUserAdmin(UserAdmin):
    # Add the 'profile' field to the User's change form
    def get_profile(self, obj):
        return obj.profile.bio if obj.profile else 'No Profile'

    get_profile.short_description = 'Profile'

    list_display = UserAdmin.list_display + ('get_profile',)
    search_fields = UserAdmin.search_fields + ('username', 'email')
    list_filter = UserAdmin.list_filter + ('is_active',)
    
    


# Unregister the default User admin and register your customized version
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
