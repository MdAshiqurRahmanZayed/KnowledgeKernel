from django.urls import path
from .views import homepage,courseDetail,createCourse,aboutCourse,myCreatedCourse,updateCourse,CreateSectionCourse,allSectionCourse,updateSection,deleteSection
urlpatterns = [
     path('',homepage,name="home"),
     path('my-courses/',myCreatedCourse,name="myCreatedCourse"),
     path('about-course/<str:slug>',aboutCourse,name="about_course"),
     
     #Course
     path('create-course/',createCourse,name="create_course"),
     path('update-course/<str:slug>/',updateCourse,name="updateCourse"),
     
     #Section
     path('create-section/<str:slug>/',CreateSectionCourse,name="create_section"),
     path('all-section/<str:slug>/',allSectionCourse,name="allSectionCourse"),
     path('update-section/course:<str:slug>/<str:section_slug>/<int:pk>',updateSection,name="update_section"),
     path('delete-section/course:<str:slug>/<str:section_slug>/<int:pk>',deleteSection,name="delete_section"),
     # path('update-section/course:<str:slug>/<str:section_slug>/',UpdateSectionCourse,name="update_section"),
     
     path('course/<slug:slug>/learn/lecture/<str:video_unique_id>/',courseDetail,name="courseDetail"),
]
