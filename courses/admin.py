from django.contrib import admin
from .models import Course,Video,SectionVideo
# Register your models here.



# class TagAdmin(admin.TabularInline):
#     model = Tag
#     extra = 1

# class VideoAdmin(admin.TabularInline):
#     model = Video
#     extra = 0
#     list_display = ("is_preview")
    
class SectionVideoAdmin(admin.TabularInline):
    model = SectionVideo
    list_display = ("course")
    extra = 0

class CourseVideoAdmin(admin.TabularInline):
    model = Video
    extra = 0

# class LearningAdmin(admin.TabularInline):
#     model = Learning
#     extra = 1

# class PrerequisiteAdmin(admin.TabularInline):
#     model = Prerequisite 
#     extra = 1
    
class CourseAdmin(admin.ModelAdmin):
    inlines = [ SectionVideoAdmin ,CourseVideoAdmin]
    prepopulated_fields = {"slug": ("name",)}  # new
    list_display = ("name","price","discount","active",)
    
class SectionVideoAdminModel(admin.ModelAdmin):
    list_display = ["name","course"] 
    prepopulated_fields = {"slug": ("name",)}  # new
    
  

class AdminVideo(admin.ModelAdmin):
     list_display = ("title","course","is_preview",)
     # list_editable = ['is_preview']
    


admin.site.register(Course,CourseAdmin)
admin.site.register(Video)
admin.site.register(SectionVideo,SectionVideoAdminModel)
