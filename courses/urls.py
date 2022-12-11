from django.urls import path
from .views import homepage,courseDetail,createCourse,aboutCourse
urlpatterns = [
     path('',homepage,name="home"),
     path('about-course/<str:slug>',aboutCourse,name="about_course"),
     path('create-course/',createCourse,name="create_course"),
     path('course/<slug:slug>/learn/lecture/<str:video_unique_id>/',courseDetail,name="courseDetail"),
]
