from django.urls import path
from .views import homepage,courseDetail
urlpatterns = [
     path('',homepage,name="home"),
     path('course/<slug:slug>/',courseDetail,name="courseDetail"),
]
