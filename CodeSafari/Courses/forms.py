from django import forms
from .models import Instructor, Student
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class InstructorForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    username = forms.CharField(max_length=150, required=True)

    class Meta:
        model = Instructor
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'bio', 'experience', 'courses', 'profile_picture']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Instructor.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered as an instructor.")
        return email

class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    date_of_birth = forms.DateField(required=True, widget=forms.SelectDateWidget(years=range(1900, 2024)))

    class Meta:
        model = Student
        fields = ['date_of_birth']  # Only include the fields relevant to the student model

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        from datetime import date
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old to register as a student.")
        return dob

    def save(self, commit=True):
        # Create the User object first and hash the password
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']  # This automatically hashes the password
        )

        # Create the Student object and associate the user with the student
        student = super().save(commit=False)
        student.user = user  # Assign the created user to the student instance

        if commit:
            student.save()
        return student
 

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)
    
class InstructorProfileForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'bio', 'experience', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }