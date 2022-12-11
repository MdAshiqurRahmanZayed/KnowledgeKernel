from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Course,Video,SectionVideo 
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import CourseCreateForm
from taggit.models import Tag 
from django.utils.text import slugify

# Create your views here.

def homepage(request):
     courses = Course.objects.filter(active=True)
     context = {
          "courses":courses
     }
     return render(request,"home.html",context)

@login_required(login_url='login')
def createCourse(request):
     if request.method == "POST":
          form = CourseCreateForm(request.POST,request.FILES)
          user = request.user.userprofile
          
          if form.is_valid():
               course = form.save(commit=False)
               course.instructor = user 
               data= form.cleaned_data.get("name")
               print(data)
               course.slug = slugify(data, allow_unicode=True)
               form.save() 
               return redirect('dashboard')
          
     else:
          form = CourseCreateForm()
     context = {
         'form':form ,
     }
     return render(request,'course/create-course.html',context)

def aboutCourse(request,slug):
     course = Course.objects.get(slug=slug)
     sections = SectionVideo.objects.filter( course__slug = slug )
     context = {
          "course":course,
          "sections":sections,
     }
     return render(request,'course/about-course.html',context)


def courseDetail(request,slug,video_unique_id):
     course = Course.objects.get( slug = slug )
     instructor = UserProfile.objects.get( user__id = course.instructor.user.id )
     sections = SectionVideo.objects.filter( course__slug = slug )
     
     # videos = Video.objects.filter(course__slug = slug).order_by("serial_number")
     # tags = Tag.objects.filter(course__slug = slug)
     # prerequisites = Prerequisite.objects.filter(course__slug = slug)
     # learnings = Learning.objects.filter(course__slug = slug)
     
     #serial number
     serial_number = request.GET.get('lecture')
     if serial_number is None:
          serial_number = 1
     video_youtube = Video.objects.get(section_video__course__slug = slug,video_unique_id = video_unique_id  )
     # user_profile  = UserProfile.objects.get(user=user)
     if request.user.is_authenticated is False and video_youtube.is_preview is False:
          return redirect('login')
     
     
     
     context = {
          'course':course,
          'sections':sections,
          # 'videos':videos,
          # 'tags':tags,
          # 'prerequisites':prerequisites,
          # 'learnings':learnings,
          'video_youtube':video_youtube,
          'instructor':instructor,
     }
     return render(request,'course/course_detail.html',context)

