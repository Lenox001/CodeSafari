from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('courses/', views.courses, name='courses'),
    path('course/<slug:slug>/', views.course_detail, name='details'),
    path('instructors/', views.instructors, name='instructors'),
    path('profile/', views.user_profile, name='profile'),
    path('instructor/profile',views.instructor_profile,name='instructor_profile'),
    path('register/instructor/', views.register_instructor, name='register_instructor'),
    path('register/student/', views.register_student, name='register_student'),
    path('login/', views.login_redirect_view, name='login'),
    path('login/instructor/', views.instructor_login, name='instructor_login'),
    path('login/student/', views.student_login, name='student_login'),
    path('instructor/dashboard/', views.instructor_dashboard, name='instructor_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('instructor/courses/', views.instructor_courses, name='instructor_courses'),
    path('forbidden/', views.forbidden, name='forbidden'),

    path('logout/', views.custom_logout, name='logout'),
]

# Serve media files during development (when `DEBUG` is True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)