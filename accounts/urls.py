from django.urls import path,include
from .views import login,register,logout,editProfile,dashboard,change_password,create_profile

urlpatterns = [
     path('',dashboard ,name="dashboard"),
     path('login/',login ,name="login"),
     path('register/',register ,name="register"),
     path('logout/',logout ,name="logout"),
     path('change-password/', change_password, name='change_password'),
     
     path('create-profile/',create_profile,name="create_profile"),
     
     path('edit-profile/',editProfile ,name="edit_profile"),
     
     
     
    
]