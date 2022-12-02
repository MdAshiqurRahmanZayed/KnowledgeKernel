from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import Course,Video,SectionVideo
# Create your views here.

def homepage(request):
     courses = Course.objects.filter(active=True)
     context = {
          "courses":courses
     }
     return render(request,"home.html",context)


def courseDetail(request,slug,video_unique_id):
     course = Course.objects.get( slug = slug )
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
     
     
     
     context = {
          'course':course,
          'sections':sections,
          # 'videos':videos,
          # 'tags':tags,
          # 'prerequisites':prerequisites,
          # 'learnings':learnings,
          'video_youtube':video_youtube,
     }
     return render(request,'course/course_detail.html',context)