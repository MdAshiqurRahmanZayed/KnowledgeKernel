from django.urls import path
from .views import homepage,courseDetail
urlpatterns = [
     path('',homepage,name="home"),
     path('course/<slug:slug>/learn/lecture/<str:video_unique_id>/',courseDetail,name="courseDetail"),
]
