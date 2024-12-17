from django.shortcuts import render, get_object_or_404, redirect
from .models import Course, Chapter, Section, Note, Instructor, Student, Profile
from django.contrib.auth.models import User
from .forms import InstructorForm, StudentRegistrationForm,CustomAuthenticationForm,InstructorProfileForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.http import HttpResponseForbidden

# Create your views here.
def home(request):
    return render(request, 'Courses/home.html')

def courses(request):
    courses = Course.objects.all()
    return render(request, 'Courses/courses.html', {'courses': courses})

def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug)
    chapters = course.chapters.all()
    return render(request, 'Courses/course_detail.html', {'course': course, 'chapters': chapters})

def instructors(request):
    instructors = Instructor.objects.all()
    return render(request, 'Courses/instructors.html', {'instructors': instructors})

def user_profile(request):
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    return render(request, 'Courses/profile.html', {'user': user, 'profile': profile})

from django.shortcuts import redirect

def register_instructor(request):
    if request.method == 'POST':
        user_form = InstructorForm(request.POST, request.FILES)

        if user_form.is_valid():
            # Extract username and email from the form
            username = user_form.cleaned_data['username']
            email = user_form.cleaned_data['email']
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "This username is already taken.")
                return render(request, 'Courses/register_instructor.html', {'user_form': user_form})

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "This email is already registered.")
                return render(request, 'Courses/register_instructor.html', {'user_form': user_form})

            # Create the User object first (don't save yet)
            user = User(username=username, email=email)

            # Create Profile for the user (do not save yet)
            profile = Profile(user=user)

            # Check if the user is approved to be an instructor
            if not profile.is_approved_instructor:
                # If not approved, redirect to forbidden page
                return redirect('forbidden')  # Redirect to the forbidden page

            # Now save the user (after approval)
            user.set_password(user_form.cleaned_data.get('password'))  # Set password before saving
            user.save()  # Save the user to the database

            # Now save the profile, linking the saved user
            profile.save()  # Save the profile after the user has been saved

            # Now create the Instructor instance and link it to the User
            instructor = user_form.save(commit=False)  # Don't save yet
            instructor.user = user  # Link the User to the Instructor
            instructor.save()  # Save the Instructor instance

            # Link profile to instructor and save
            instructor.profile = profile
            instructor.save()

            # Assign user role as instructor (if approved)
            user.is_staff = True  # Set is_staff to True for instructors
            user.save()

            # Redirect to instructor login page after registration
            return redirect('instructor_login')  # Redirect to the instructor login page
    else:
        user_form = InstructorForm()

    return render(request, 'Courses/register_instructor.html', {'user_form': user_form})


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form which will create the user and student
            return redirect('student_login')  # Redirect to home after registration
    else:
        form = StudentRegistrationForm()

    return render(request, 'Courses/register_student.html', {'form': form})


# Login for Instructor
def instructor_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if user.is_staff:
                    login(request, user)
                    return redirect('instructor_dashboard')  # Redirect to the instructor dashboard
                else:
                    messages.error(request, "You are not authorized to access the instructor portal.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'Courses/instructor_login.html', {'form': form})

def student_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                if not user.is_staff:
                    login(request, user)
                    return redirect('student_dashboard')  # Redirect to the student dashboard
                else:
                    messages.error(request, "You are not authorized to access the student portal.")
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'Courses/student_login.html', {'form': form})


@login_required
def instructor_dashboard(request):
    # Instructor dashboard logic here
    return render(request, 'Courses/instructor_dashboard.html')

@login_required
def student_dashboard(request):
    # Student dashboard logic here
    return render(request, 'Courses/student_dashboard.html')

def custom_logout(request):
    logout(request)
    
    # Redirect based on user role after logout
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('instructor_login')  # Redirect to instructor login
        else:
            return redirect('student_login')  # Redirect to student login
    else:
        # Redirect to the login page (if the user wasn't logged in before)
        return redirect('login')  # Replace 'login' with your actual login page URL

    
def login_redirect_view(request):
    if request.user.is_authenticated:
        # Redirect the user based on role
        if request.user.is_staff:
            return redirect('instructor_dashboard')  # Redirect to instructor dashboard if staff
        else:
            return redirect('student_dashboard')  # Redirect to student dashboard if not staff
    
    # If not authenticated, render the role selection page
    return render(request, 'Courses/login.html')  # Replace this with your login page


@login_required
def instructor_profile(request):
    user = request.user
    profile = Instructor.objects.filter(email=user.email).first()  # Retrieve the instructor's profile

    if not profile:
        return render(request, 'Courses/instructor_profile.html', {'error': "Profile not found."})

    if request.method == "POST":
        form = InstructorProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('instructor_profile')
    else:
        form = InstructorProfileForm(instance=profile)

    return render(request, 'Courses/instructor_profile.html', {'form': form, 'profile': profile})

def instructor_home(request):
    return render(request,'Courses/instructor_home.html')

@login_required
def instructor_courses(request):
    # Get the instructor associated with the logged-in user
    try:
        instructor = Instructor.objects.get(email=request.user.email)
    except Instructor.DoesNotExist:
        return render(request, 'error.html', {'message': 'Instructor profile not found.'})

    # Fetch courses taught by the instructor
    courses = instructor.courses.all()

    # Render template with courses and instructor details
    return render(
        request, 
        'Courses/instructor_courses.html', 
        {'instructor': instructor, 'courses': courses}
    )
    
def forbidden(request):
    return render(request, 'Courses/forbidden.html') 