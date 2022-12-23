from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Course,Video,SectionVideo,Assessment,SubmittedAssessment
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import CourseCreateForm,SectionForm,VideoForm,AssessmentForm,SubmittedAssessmentForm,MarkForm
from taggit.models import Tag 
from django.utils.text import slugify
from django.contrib import messages,auth
from accounts.models import *
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
     courses = Course.objects.filter(instructor = request.user.userprofile).order_by('-created_at')
     context = {
          "createdCourse":createdCourse,
          "courses":courses
     }
     
     return render(request,'course/my_courses.html',context)




#course

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
     count = Assessment.objects.filter(course__slug = slug).count()

     
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
          'count':count,
          'video_youtube':video_youtube,
          'instructor':instructor,
     }
     return render(request,'course/course_detail.html',context)





# Course CRUD
@login_required(login_url='login')
def createCourse(request):
     if request.method == "POST":
          form = CourseCreateForm(request.POST,request.FILES)
          user = request.user.userprofile
          
          if form.is_valid():
               course = form.save( commit = False)
               course.instructor = user 
               data = form.cleaned_data.get("name")
               course.slug = slugify(data, allow_unicode=True)
               form.save()
               course.save() 
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
          form = CourseCreateForm(request.POST, request.FILES , instance = course)          
          if form.is_valid():
               course_update = form.save( commit = False)
               data = form.cleaned_data.get("name")
               course_update.slug = slugify(data, allow_unicode=True)
               # tags = form.cleaned_data.get("tags")
               
               
               # course.tags = tags
               form.save()
               course_update.save() 
               messages.success(request, 'Your Course has been Updated Successfully.')
               return redirect('myCreatedCourse')
          
     else:
          form = CourseCreateForm(instance = course )
          
     context = {
         'form':form ,
         'course':course
     }
     return render(request,'course/create-course.html',context)

def deleteCourse(request,slug):
     course = Course.objects.get(slug=slug)
     if request.method == "POST":
          try:
               course.delete()
               messages.info(request,'Your Course has been deleted successfully.')
               return redirect('dashboard')
          except:
               messages.info(request,'Please try again')
               return redirect('dashboard')
          
     
     context = {
          "course":course
     }
     return render(request,'course/delete-course.html',context)


# section CRUD
@login_required(login_url='login')
def CreateSectionCourse(request,slug):
     course = Course.objects.get(slug=slug)
     if request.method == "POST":
          form = SectionForm(request.POST)
          try:
               if form.is_valid():
                    section_name = form.cleaned_data.get("name")
                    section_slug = slugify(section_name ,allow_unicode=True)    
                    section = form.save(commit=False)
                    
                    section.course = course
                    section.slug = section_slug
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
          messages.success(request, 'Your Section has been Deleted Successfully.')
          section.delete()
          return redirect('allSectionCourse',slug)
     context = {
          "course":course,
          "section":section,
          # "form": form
     }
     return render(request,'course/delete-section.html',context)



# Video CRUD
@login_required(login_url='login')
def createSectionVideo(request,slug):
     course = Course.objects.get(slug=slug)
     sections = SectionVideo.objects.filter(course__slug = slug).order_by('serial_number')
     count = Video.objects.filter(course__slug = slug).count()
     context = {
          "sections": sections,
          "course":course,
          "count":count,
     }


     return render(request,'course/video-section.html',context)


@login_required(login_url='login')
def allSectionVideo(request,slug):
     course = Course.objects.get(slug=slug)
     sections = SectionVideo.objects.filter( course__slug = slug )
     count = Video.objects.filter(course__slug = slug).count()
     context = {
          "course":course,
          "sections":sections,
          "count":count,
     }
     return render(request,'course/all-section-video.html',context)



@login_required(login_url='login')
def createVideo(request,slug,section_slug,pk):
     course = Course.objects.get(slug=slug)
     section = SectionVideo.objects.get(id=pk)
     if request.method == "POST":
          form = VideoForm(request.POST)          
          if form.is_valid():
               course_video = form.save(commit=False)
               course_video.section_video = section
               course_video.course = course
               course_video.save()
               messages.success(request, 'Your video has been Created.')
               return redirect('allSectionVideo' ,slug)
     else:
          form = VideoForm()
     context = {
          "course":course,
          "form":form,
     }
     return render(request,'course/video-form.html',context)



@login_required(login_url='login')
def updateVideo(request,slug,section_slug,video_unique_id):
     course = Course.objects.get(slug=slug)
     video = Video.objects.get(course__slug = slug,video_unique_id = video_unique_id )
     if request.method == "POST":
          form = VideoForm(request.POST,instance = video)          
          if form.is_valid():
               course_video = form.save(commit=False)
               course_video.course = course
               course_video.save()
               messages.success(request, 'Your video has been Updated successfully.')
               return redirect('allSectionVideo' ,slug)
     else:
          form = VideoForm(instance = video)
     context = {
          "course":course,
          "form":form,
     }
     return render(request,'course/video-form.html',context)


@login_required(login_url='login')
def deleteVideo(request,slug,section_slug,video_unique_id):
     course = Course.objects.get(slug=slug)
     delete = Video.objects.get(course__slug = slug,video_unique_id = video_unique_id )
     if request.method == "POST":
          messages.success(request, 'Your Video has been Deleted Successfully.')
          delete.delete()
          return redirect('allSectionVideo' ,slug)

     context = {
          "course":course,
          "delete":delete,
     }
     return render(request,'course/delete-verify.html',context)


# Assessment CRUD
@login_required(login_url='login')
def allAssessment(request,slug):
     course = Course.objects.get(slug=slug)
     assessments = Assessment.objects.filter( course__slug = slug ).order_by('-created_at')
     count = Assessment.objects.filter(course__slug = slug).count()
     context = {
          "course":course,
          "assessments":assessments,
          "count":count,
     }
     return render(request,'course/all-assessment.html',context)


@login_required(login_url='login')
def createAssessment(request,slug):
     course = Course.objects.get(slug=slug)
     if request.method == "POST":
          form = AssessmentForm(request.POST)
          try:
               if form.is_valid():
                    assessment = form.save(commit=False)
                    assessment.course = course
                    assessment.save()
                    messages.success(request, 'Your Assessment has been Created successfully.')
                    return redirect('allAssessment' ,slug)
          except:
               messages.danger(request, 'Your Assessment has not been Created.')
               return redirect('allAssessment',slug)
     else:
          form = AssessmentForm()
     context = {
          "course": course,
          "form" :form
     }
     return render(request,'course/assessment-form.html',context)

@login_required(login_url='login')
def updateAssessment(request,slug,pk):
     course = Course.objects.get(slug=slug)
     assessment = Assessment.objects.get(id = pk)
     if request.method == "POST":
          form = AssessmentForm(request.POST ,instance = assessment)
          try:
               if form.is_valid():
                    form.save()
                    messages.success(request, 'Your Assessment has been Updated successfully.')
                    return redirect('allAssessment' ,slug)
          except:
               messages.danger(request, 'Your Assessment has not been Updated.')
               return redirect('allAssessment',slug)
     else:
          form = AssessmentForm(instance = assessment)
     context = {
          "course": course,
          "form" :form
     }
     return render(request,'course/assessment-form.html',context)



@login_required(login_url='login')
def updateAssessment(request,slug,pk):
     course = Course.objects.get(slug=slug)
     assessment = Assessment.objects.get(id = pk)
     if request.method == "POST":
          form = AssessmentForm(request.POST ,instance = assessment)
          try:
               if form.is_valid():
                    form.save()
                    messages.success(request, 'Your Assessment has been Updated successfully.')
                    return redirect('allAssessment' ,slug)
          except:
               messages.danger(request, 'Your Assessment has not been Updated.')
               return redirect('allAssessment',slug)
     else:
          form = AssessmentForm(instance = assessment)
     context = {
          "course": course,
          "form" :form
     }
     return render(request,'course/assessment-form.html',context)



@login_required(login_url='login')
def deleteAssessment(request,slug,pk):
     course = Course.objects.get(slug=slug)
     delete = Assessment.objects.get(id = pk)
     if request.method == "POST":
          messages.success(request, 'Your Assessment has been Deleted Successfully.')
          delete.delete()
          return redirect('allAssessment' ,slug)

     context = {
          "course":course,
          "delete":delete,
     }
     return render(request,'course/delete-verify.html',context)


#show Assessment
def showAllAssessment(request,slug):
     course = Course.objects.get(slug=slug)
     assessment = Assessment.objects.filter(course = course)
     marks = SubmittedAssessment.objects.filter(course = course,student_user=request.user)
     
     context = {
          "course" : course,
          "assessment" : assessment,
          "marks" : marks,
     }
     return render(request,'course/show-all-assessment.html',context)

def submitAssessment(request,slug,pk):
     course = Course.objects.get(slug=slug)
     assessment = Assessment.objects.get(id = pk)
     if request.method =="POST":
          form = SubmittedAssessmentForm(request.POST)
          submitted_answer = form.save(commit=False)
          submitted_answer.student_user = request.user
          submitted_answer.assessment = assessment 
          submitted_answer.course = course 
          submitted_answer.save()
          messages.success(request, 'Your Answer has been stored Successfully.')
          return redirect('showAllAssessment',slug)
     else:
          form = SubmittedAssessmentForm()
     context = {
          "course" : course,
          "assessment" : assessment,
          "form" : form,
     }
     return render(request,'course/submit-assessment.html',context)


def updateAssessment(request,slug,pk):
     course = Course.objects.get(slug = slug)
     submitted_assessment = SubmittedAssessment.objects.get( id = pk)
     print(submitted_assessment)
     if request.method == "POST":
          form = SubmittedAssessmentForm(request.POST,instance = submitted_assessment)
          form.save()
          return redirect('showAllAssessment',slug)
     else:
          form = SubmittedAssessmentForm( instance = submitted_assessment)
     context = {
          "course" : course,
          "form" : form,
     }
     return render(request,'course/submit-assessment.html',context) 



#mark Assessment

def showAllSubmittedAssessmentUser(request,slug):
     course = Course.objects.get(slug = slug)
     count = SubmittedAssessment.objects.filter(course__slug = slug ).count()
     users = Account.objects.all()
     
     
     
     context = {
          "course" : course,
          "count" : count,
          "users" : users,
     }

     return render(request,'course/show-submitted-user.html',context)


def showAllSubmittedAssessmentDetail(request,slug,student_user):
     course = Course.objects.get(slug = slug)
     submitted_assesments = SubmittedAssessment.objects.filter(course__slug = slug , student_user = student_user  ).order_by('assessment')
     count = SubmittedAssessment.objects.filter(course__slug = slug , student_user = student_user  ).count()

     context = {
          "course" : course,
          "submitted_assesments" : submitted_assesments,
          "count" : count,
     }
     return render(request,'course/show-submitted-assessment-detail.html',context)

def markAssessment(request,slug,assessment_pk,submitted_pk,student_user):
     course = Course.objects.get(slug = slug)
     assessment = Assessment.objects.get(id = assessment_pk)
     submit_ssessment = SubmittedAssessment.objects.get(id = submitted_pk)
     if request.method =="POST":
          form = MarkForm(request.POST,instance=submit_ssessment)
          try:
               if form.is_valid():
                    form.save()
                    messages.success(request, 'Your mark has been stored.')
                    return redirect('showAllSubmittedAssessmentDetail', slug, student_user)
               else:
                    messages.info(request, 'Your mark has not been stored.')
                    return redirect('showAllSubmittedAssessmentDetail', slug, student_user)
          except:
               messages.info(request, 'Your mark has not been stored.')
               return redirect('showAllSubmittedAssessmentDetail', slug, student_user)
     else:
               form = MarkForm(instance=submit_ssessment)
     
     context = {
          'form':form,
          'course':course,
          'assessment':assessment,
     }
     return render(request,'course/mark.html',context)