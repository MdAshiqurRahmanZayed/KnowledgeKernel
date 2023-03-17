from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import Course,Video,SectionVideo,Assessment,SubmittedAssessment,EnrolledCourse,Category,EnrolledCourse,Payment
from accounts.models import UserProfile
from django.contrib.auth.decorators import login_required
from .forms import CourseCreateForm,SectionForm,VideoForm,AssessmentForm,SubmittedAssessmentForm,MarkForm
from taggit.models import Tag 
from django.utils.text import slugify
from django.contrib import messages,auth
from accounts.models import *
from django.db.models import Q 
from mptt.templatetags.mptt_tags import tree_info 
from django.core.paginator import EmptyPage,PageNotAnInteger,Paginator
from sslcommerz_lib import SSLCOMMERZ 
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from courses.sslcommerz import initiate_payment
from django.conf import settings
import json
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.

def homepage(request):
     courses = Course.objects.filter(active=True)
     courses_count = Course.objects.filter(active=True).count()
     top_course = Course.objects.filter(top_course = True)
     categories = Category.objects.all()
     context = {
          "courses":courses,
          "courses_count":courses_count,
          "top_course":top_course,
          "categories":categories,
          'tree_info': tree_info(categories),
     }
     return render(request,"home.html",context)



@login_required(login_url='login')
def myCreatedCourse(request):
     createdCourse = Course.objects.filter(instructor = request.user.userprofile).count()
     courses = Course.objects.filter(instructor = request.user.userprofile).order_by('-created_at')
     # memberCount = Course.objects.filter(instructor = request.user.userprofile).count()
     context = {
          "createdCourse":createdCourse,
          "courses":courses
     }
     
     return render(request,'course/my_courses.html',context)


@login_required(login_url='login')
def myCourses(request):
     enrolledCourseCount = EnrolledCourse.objects.filter(user = request.user).count()
     enrolledCourse = EnrolledCourse.objects.filter(user = request.user).order_by('-created_at')
     # memberCount = Course.objects.filter(instructor = request.user.userprofile).count()
     context = {
          "enrolledCourseCount":enrolledCourseCount,
          "enrolledCourse":enrolledCourse
     }
     
     return render(request,'course/my_courses.html',context)



def allCourses(request):
     courses = Course.objects.filter(active=True).order_by( '-id')
     courses_count = Course.objects.filter(active=True).count()
     top_course = Course.objects.filter(top_course = True)
     categories = Category.objects.all()
     
     #pagination
     paginator = Paginator(courses,2)
     page = request.GET.get('page')
     pagedCourses = paginator.get_page(page)
     
     
     context = {
          "courses":pagedCourses,
          "courses_count":courses_count,
          "top_course":top_course,
          "categories":categories,
          'tree_info': tree_info(categories),
     }
     return render(request,'course/all-courses.html',context)


#Enrolled Course




#course

def aboutCourse(request,slug):
     course = Course.objects.get(slug=slug)
     sections = SectionVideo.objects.filter( course__slug = slug ) 
     enrolled = EnrolledCourse.objects.all()
     enrolled_person = []
     store_id = settings.STORE_ID
     store_pass = settings.STORE_PASS
     # settings = { 'store_id': store_id, 'store_pass': store_pass, 'issandbox': True }
     for i in enrolled:
          enrolled_person.append( i.user)
     if request.user in enrolled_person:
          try:
               check_enrolled = EnrolledCourse.objects.get(user = request.user,course = course,enrolled=True)
          except:
               
               check_enrolled = False 
     else:
               check_enrolled = False 
          
     # try:
     #      check_enrolled = EnrolledCourse.objects.get(user = request.user,course = course,enrolled=False)
     # except:
     #      check_enrolled = EnrolledCourse.objects.get(user = request.user,course = course)
     if request.method == "POST" and check_enrolled == False:
     # if request.method == "POST" :
          # EnrolledCourse.objects.create(user = request.user,course = course,enrolled=True)
          # print("test")
          obj = EnrolledCourse(user = request.user,course = course,enrolled=True)
          obj.save()
          return redirect('dashboard')
     else:
          redirect("about_course",slug)
     
     context = {
          "course":course,
          "sections":sections,
          "check_enrolled":check_enrolled,
     }
     return render(request,'course/about-course.html',context)
@login_required(login_url='login')
@csrf_exempt
def initiate(request,pk):
    course =  Course.objects.get(id = pk)
    if request.method == 'POST':
        if course.price <=0:
             amount = 0
        else:
             amount = course.price - (course.price*course.discount*.01)
        email = request.user
        user= UserProfile.objects.get(user = request.user)
        phone = user.phone_number 
        user  = Account.objects.get(id = request.user.id)        
        current_site = get_current_site(request)
        response_data = initiate_payment(amount, email, phone,course.id,user.id ,current_site)
        return redirect(response_data['GatewayPageURL'])
    else:
        return render(request, 'course/payment_gateway/index.html',{'course':course})
# @login_required(login_url='login')
@csrf_exempt
def success(request,user_id,course_id):
    # Get the payment data from the session
    course = Course.objects.get(id = course_id)
    payment_data = request.POST
#     print(payment_data['cus_email'])
#     print(payment_data)
    if not payment_data:
        return redirect('home')
    
    user  = Account.objects.get(id = user_id)
    print(user)
    # Get the transaction ID from the query string
#     val_id = payment_data['cus_email']
    print(request)
#     user  = Account.objects.get(user = request.user)
#     print(payment_data.keys())
#     print(payment_data['course_id'])
    payment = Payment.objects.create(
        user=user,
     #     user= user,
     #    transaction_id=payment_data['tran_id'],
        amount=payment_data['amount'],
     #    currency=payment_data['currency'],
        description=course.name,
        status=payment_data['status'],
        val_id=payment_data['val_id'],
        
    )
    EnrolledCourse.objects.create(user = user , course = course , enrolled = True)
    return redirect('dashboard')

    # Render the success template with the payment object
#     return render(request, 'course/payment_gateway/success.html', {'payment': payment})
@csrf_exempt
def failPayment(request,course_id):
     course = Course.objects.get(id = course_id)
     
     context = {
          'course':course
     }
     return render(request, 'course/payment_gateway/fail.html',context)



def viewCourseCategoriesWise(request,slug):
     courses = Course.objects.filter(active=True ,categories__slug  = slug).order_by('-id')
     category = Category.objects.get(slug=slug)
     courses_count = courses.count()
     top_course = Course.objects.filter(top_course = True)
     categories = Category.objects.all() 
     
     #pagination
     paginator = Paginator(courses,2)
     page = request.GET.get('page')
     pagedCourses = paginator.get_page(page)
     context = {
          "courses":pagedCourses,
          "courses_count":courses_count,
          "top_course":top_course,
          "categories":categories,
          "category":category,
          'tree_info': tree_info(categories),
     }
     return render(request,'course/all-courses.html',context)


def courseDetail(request,slug,video_unique_id):
     course = Course.objects.get( slug = slug )
     instructor = UserProfile.objects.get( user__id = course.instructor.user.id )
     sections = SectionVideo.objects.filter( course__slug = slug )
     count = Assessment.objects.filter(course__slug = slug).count()
     try:
          enrolled = EnrolledCourse.objects.filter(  course__slug = slug,user = request.user).exists()
     except:
          enrolled = "Please enroll to see all the assessment."

     
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
          'enrolled':enrolled,
     }
     return render(request,'course/course_detail.html',context)


def searchCourse(request):
     if 'keyword' in request.GET:
          keyword = request.GET['keyword']
          
          if keyword:
               courses  = Course.objects.order_by('-created_at').filter(Q(name__icontains = keyword) | Q(description__icontains = keyword))
               courses_count  = courses.count()
          context = {
               "courses":courses,
               "courses_count":courses_count,
               "keyword":keyword,
          } 
     return render(request,"course/all-courses.html",context)



#all tags
@login_required(login_url='login')
def allTags(request):
     tags = Tag.objects.all().order_by('name')
     context = {
          'tags':tags
     }
     
     
     return render(request,'course/all-tags.html',context)




# Course CRUD
@login_required(login_url='login')
def createCourse(request):
     if UserProfile.objects.filter(user__email = request.user.email).exists() == False:
          messages.warning(request,"Please Complete Your Profile")
          return redirect('create_profile')
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
          try:         
               if form.is_valid():
                    course_update = form.save( commit = False)
                    data = form.cleaned_data.get("name")
                    course_update.slug = slugify(data, allow_unicode=True)
                    # tags = form.cleaned_data.get("tags")
                    
                    
                    # course.tags = tags
                    form.save()
                    course_update.save() 
                    messages.success(request, 'Your Course has been Updated Successfully.')
                    return redirect('updateCourse',slug)
          except:
                    return redirect('updateCourse',slug)
          
     else:
          form = CourseCreateForm(instance = course )
          
     context = {
         'form':form ,
         'course':course
     }
     return render(request,'course/create-course.html',context)


@login_required(login_url='login')
def deleteCourse(request,slug):
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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
@login_required(login_url='login')
def showAllAssessment(request,slug):
     course = get_object_or_404(Course,slug = slug )
     assessment = Assessment.objects.filter(course = course)
     submitted_assessments = SubmittedAssessment.objects.filter(course = course )
     marks = SubmittedAssessment.objects.filter(course = course,student_user__id=request.user.id) 
     enrolled_user = EnrolledCourse.objects.get(course__slug = slug ,user__id=request.user.id)
     
     context = {
          "course" : course,
          "assessment" : assessment,
          "marks" : marks,
          "submitted_assessments" : submitted_assessments,
          "enrolled_user" : enrolled_user,
     }
     return render(request,'course/show-all-assessment.html',context)


@login_required(login_url='login')
def submitAssessment(request,slug,pk):
     course = Course.objects.get(slug=slug)
     assessment = Assessment.objects.get(id = pk)
     student_user = EnrolledCourse.objects.get(user = request.user)
     if request.method =="POST":
          form = SubmittedAssessmentForm(request.POST)
          submitted_answer = form.save(commit=False)
          submitted_answer.student_user = student_user
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

@login_required(login_url='login')
def updateAssessmentUser(request,slug,pk,student_user):
     course = Course.objects.get(slug = slug)
     assessment = Assessment.objects.get(id = pk)
     submitted_assessment = SubmittedAssessment.objects.get( course = course,assessment = assessment,student_user__user__id = student_user )
     if request.method == "POST":
          form = SubmittedAssessmentForm(request.POST,instance = submitted_assessment)
          form.save()
          messages.success(request, 'Your Answer has been Updated Successfully.')
          return redirect('showAllAssessment',slug)
     else:
          form = SubmittedAssessmentForm( instance = submitted_assessment)
     context = {
          "course" : course,
          "form" : form,
     }
     return render(request,'course/submit-assessment.html',context) 


@login_required(login_url='login')
def submitOrUpdateAssessmentUser(request,slug,pk,student_user):
     course = Course.objects.get(slug=slug)
     assessment = Assessment.objects.get(id = pk)
     try:
          test = EnrolledCourse.objects.filter(user__id = student_user)
          # print(test[0][0])
          test = True
     except:
          test = False
     try:
          submitted_assessment = SubmittedAssessment.objects.get( course__slug = slug,assessment__id = pk,student_user__id = student_user )
          if request.method == "POST":
               form = SubmittedAssessmentForm(request.POST,instance = submitted_assessment)
               form.save()
               messages.success(request, 'Your Answer has been Updated Successfully.')
               return redirect('showAllAssessment',slug)
          else:
               form = SubmittedAssessmentForm( instance = submitted_assessment)
     except:
          # student = EnrolledCourse.objects.get(user__id = request.user.id)
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
     



#mark Assessment
@login_required(login_url='login')
def showAllSubmittedAssessmentUser(request,slug):
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
     count = SubmittedAssessment.objects.filter(course__slug = slug ).count()
     users = EnrolledCourse.objects.filter(course__slug = slug)     
     users_count = EnrolledCourse.objects.filter(course__slug = slug).count()     
     context = {
          "course" : course,
          "count" : count,
          "users" : users,
          "users_count" : users_count,
     }

     return render(request,'course/show-submitted-user.html',context)

@login_required(login_url='login')
def submittedUserSearch(request,slug):
     if 'keyword' in request.GET:
          keyword = request.GET['keyword']
          # users = EnrolledCourse.objects.filter(course__slug = slug).filter(user__email__icontains=keyword)
          users = EnrolledCourse.objects.filter(course__slug = slug)
          users = users.filter( user__email__icontains = keyword)     
          # print(users.filter(user__email__icontains = keyword))
          count = users.count()
     else:
          users = EnrolledCourse.objects.filter(course__slug = slug)     
          count = SubmittedAssessment.objects.filter(course__slug = slug ).count()
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
     context = {
          "course" : course,
          "count" : count,
          "users" : users,
     }
     return render(request,'course/show-submitted-user.html',context)
     


@login_required(login_url='login')
def showAllSubmittedAssessmentDetail(request,slug,student_user):
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
     submitted_assesments = SubmittedAssessment.objects.filter(course__slug = slug ,student_user__id = student_user  ).order_by('-assessment')
     count = SubmittedAssessment.objects.filter(course__slug = slug, student_user__id=student_user ).count()

     context = {
          "course" : course,
          "submitted_assesments" : submitted_assesments,
          "count" : count,
     }
     return render(request,'course/show-submitted-assessment-detail.html',context)

def markAssessment(request,slug,assessment_pk,submitted_pk,student_user):
     course = get_object_or_404(Course,slug = slug ,instructor=request.user.userprofile)
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