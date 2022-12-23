from django.urls import path
from .views import *
urlpatterns = [
     path('',homepage,name="home"),
     path('my-courses/',myCreatedCourse,name="myCreatedCourse"),
     path('about-course/<str:slug>',aboutCourse,name="about_course"),
     
     #Course
     path('create-course/',createCourse,name="create_course"),
     path('update-course/<str:slug>/',updateCourse,name="updateCourse"),
     path('delete-course/<str:slug>/',deleteCourse,name="deleteCourse"),
     
     #Section
     path('create-section/<str:slug>/',CreateSectionCourse,name="create_section"),
     path('all-section/<str:slug>/',allSectionCourse,name="allSectionCourse"),
     path('update-section/course:<str:slug>/<str:section_slug>/<int:pk>',updateSection,name="update_section"),
     path('delete-section/course:<str:slug>/<str:section_slug>/<int:pk>',deleteSection,name="delete_section"),
     # path('update-section/course:<str:slug>/<str:section_slug>/',UpdateSectionCourse,name="update_section"),
     
     #Video
     path('all-section-video/<str:slug>/',allSectionVideo,name="allSectionVideo"),
     path('create-video/<str:slug>/',createSectionVideo,name="createSectionVideo"),
     path('create-video/<str:slug>/video-section=<str:section_slug>/<int:pk>/',createVideo,name="create_video"),
     path('update-video/<str:slug>/video-section=<str:section_slug>/<str:video_unique_id>/',updateVideo,name="update_video"),
     path('delete-video/<str:slug>/video-section=<str:section_slug>/<str:video_unique_id>/',deleteVideo,name="delete_video"),
     
     #Assessment
     path('all-assessment/<str:slug>/',allAssessment,name="allAssessment"),
     path('create-assessment/<str:slug>/',createAssessment,name="createAssessment"),
     path('update-assessment/course:<str:slug>/<int:pk>',updateAssessment,name="updateAssessment"),
     path('delete-assessment/course:<str:slug>/<int:pk>',deleteAssessment,name="deleteAssessment"),
     
     #Show Assessment
     path('assessment-course/<str:slug>/',showAllAssessment,name="showAllAssessment"),
     path('assessment-course/<str:slug>/assessment/<int:pk>/',submitAssessment,name="submitAssessment"),
     path('update-assessment-course/<str:slug>/assessment/<int:pk>/',updateAssessment,name="updateAssessment"),
     
     #marks
     path('submitted-user-course/<str:slug>/',showAllSubmittedAssessmentUser,name="showAllSubmittedAssessmentUser"),
     path('course/<str:slug>/all-submitted-assessment/<str:student_user>/',showAllSubmittedAssessmentDetail,name="showAllSubmittedAssessmentDetail"),
     path('course/<str:slug>/mark-assessment/assessment/<int:assessment_pk>/submitted-assessment/<int:submitted_pk>/submitted-user/<int:student_user>/',markAssessment,name="markAssessment"),
     
     
     
     
     path('course/<slug:slug>/learn/lecture/<str:video_unique_id>/',courseDetail,name="courseDetail"),
]
