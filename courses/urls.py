from django.urls import path
from .views import *
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
     
     #Video
     path('all-section-video/<str:slug>/',allSectionVideo,name="allSectionVideo"),
     path('create-video/<str:slug>/',createSectionVideo,name="createSectionVideo"),
     path('create-video/<str:slug>/video-section=<str:section_slug>/<int:pk>/',createVideo,name="create_video"),
     path('update-video/<str:slug>/video-section=<str:section_slug>/<str:video_unique_id>/',updateVideo,name="update_video"),
     path('delete-video/<str:slug>/video-section=<str:section_slug>/<str:video_unique_id>/',deleteVideo,name="delete_video"),
     
     
     
     path('course/<slug:slug>/learn/lecture/<str:video_unique_id>/',courseDetail,name="courseDetail"),
]
