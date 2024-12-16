from django.shortcuts import render
from .models import Course

# Create your views here.
def home(request):
    courses=Course.objects.all()
    return render(request,'Courses/home.html',{'courses':courses})
