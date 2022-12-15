from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Course,Video,SectionVideo 
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import CourseCreateForm,CourseActivation,SectionForm
from taggit.models import Tag 
from django.utils.text import slugify
from django.contrib import messages,auth

# Create your views here.

def homepage(request):
     courses = Course.objects.filter(active=True)
     context = {
          "courses":courses
     }
     return render(request,"home.html",context)

@login_required(login_url='login')
def myCreatedCourse(request):
     createdCourse = Course.objects.filter(instructor = request.user.userprofile).count()
     courses = Course.objects.filter(instructor = request.user.userprofile).order_by('-date')
     context = {
          "createdCourse":createdCourse,
          "courses":courses
     }
     
     return render(request,'course/my_courses.html',context)

# Course
@login_required(login_url='login')
def createCourse(request):
     if request.method == "POST":
          form = CourseCreateForm(request.POST,request.FILES)
          user = request.user.userprofile
          
          if form.is_valid():
               course = form.save(commit=False)
               course.instructor = user 
               data = form.cleaned_data.get("name")
               course.slug = slugify(data, allow_unicode=True)
               form.save() 
               messages.success(request, 'Your Course has been Created.')
               
               return redirect('myCreatedCourse')
          
     else:
          form = CourseCreateForm(request.POST or None)
     context = {
         'form':form ,
     }
     return render(request,'course/create-course.html',context)


@login_required(login_url='login')
def updateCourse(request,slug):
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
     if request.method == "POST":
          form = CourseCreateForm(request.POST,request.FILES ,instance = course)          
          if form.is_valid():
               course = form.save(commit=False)
               data = form.cleaned_data.get("name")
               course.slug = slugify(data, allow_unicode=True)
               messages.success(request, 'Your Course has been Updated Successfully.')
               
               form.save() 
               return redirect('myCreatedCourse')
          
     else:
          form = CourseCreateForm(instance = course )
          
     context = {
         'form':form ,
         'course':course
     }
     return render(request,'course/create-course.html',context)



# section
@login_required(login_url='login')
def CreateSectionCourse(request,slug):
     course = Course.objects.get(slug=slug)
     print(course)
     if request.method == "POST":
          form = SectionForm(request.POST)
          try:
               if form.is_valid():
                    section_name = form.cleaned_data.get("name")
                    section_slug = slugify(section_name ,allow_unicode=True)    
                    section = form.save(commit=False)
                    
                    section.course = course
                    section.slug = section_slug
                    print(section_slug)
                    section.save()                 
                    messages.success(request, 'Your Section has been Created Successfully.')
                    return redirect('allSectionCourse',slug)
          except:
               return redirect('create_section')
     else:
          form = SectionForm()
     context = {
          "course": course,
          "form" :form
     }
     return render(request,'course/section-form.html',context)

@login_required(login_url='login')
def allSectionCourse(request,slug):
     course = Course.objects.get(slug=slug)
     sections = SectionVideo.objects.filter(course__slug = slug).order_by('serial_number')
     count = SectionVideo.objects.filter(course__slug = slug).count()

     context = {
          "sections": sections,
          "course":course,
          "count":count,
     }
     return render(request,'course/course-section.html',context)


@login_required(login_url='login')
def updateSection(request,slug,section_slug,pk):
     course = Course.objects.get(slug=slug)
     data = SectionVideo.objects.get(course = course  , course__instructor = request.user.userprofile,  slug = section_slug,id=pk)
     if request.method == "POST":
          form = SectionForm(request.POST, instance = data)
          try:
               if form.is_valid():
                    section = form.save(commit=False)
                    data = form.cleaned_data.get("name")
                    section.slug = slugify(data, allow_unicode=True)
                    
                    messages.success(request, 'Your Section has been Updated Successfully.')
                    section.save() 
                    return redirect('allSectionCourse',slug)
          except:
               pass   
          
     else:
          form = SectionForm(instance = data)
     
     context = {
          "course":course,
          "form": form
     }
     return render(request,'course/section-form.html',context)

@login_required(login_url='login')
def deleteSection(request,slug,section_slug,pk):
     course = Course.objects.get(slug=slug)
     section = SectionVideo.objects.get(course__slug = slug,course__instructor = request.user.userprofile,slug= section_slug,id=pk)
     if request.method == "POST":
          section.delete()
          return redirect('allSectionCourse',slug)
     context = {
          "course":course,
          "section":section,
          # "form": form
     }
     return render(request,'course/delete-section.html',context)



# def UpdateSectionCourse(request,slug,section_slug):
#      course = Course.objects.get(slug=slug)
#      print(course)
#      if request.method == "POST":
#           form = SectionForm(request.POST ,instance=course)
#           try:
#                if form.is_valid():
#                     section_name = form.cleaned_data.get("name")
#                     section_new_slug = slugify(section_name ,allow_unicode=True)    
#                     section = form.save(commit=False)
                    
#                     section.course = course
#                     section.slug = section_new_slug
#                     print(section_new_slug)
#                     section.save()                 
#                     return redirect('home')
#           except:
#                return redirect('create_section')
#      else:
#           form = SectionForm(instance=course)
#      context = {
#           "course": course,
#           "form" :form
#      }
#      return render(request,'course/section-form.html',context)











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

