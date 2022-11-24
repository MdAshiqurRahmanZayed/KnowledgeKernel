from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Course
# Create your views here.

def homepage(request):
     courses = Course.objects.all()
     
     context = {
          "courses":courses
     }
     return render(request,"home.html",context)