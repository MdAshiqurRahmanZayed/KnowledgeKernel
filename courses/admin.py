from django.contrib import admin
from .models import Course,Tag,Prerequisite,Learning,Video
# Register your models here.


class TagAdmin(admin.TabularInline):
    model = Tag
    extra = 1

class VideoAdmin(admin.TabularInline):
    model = Video
    list_display = ("is_preview")

class LearningAdmin(admin.TabularInline):
    model = Learning
    extra = 1

class PrerequisiteAdmin(admin.TabularInline):
    model = Prerequisite 
    extra = 1
    
class CourseAdmin(admin.ModelAdmin):
    inlines = [TagAdmin , LearningAdmin , PrerequisiteAdmin,VideoAdmin ]
    prepopulated_fields = {"slug": ("name",)}  # new
    list_display = ("name","price","discount","active",)
    
class AdminVideo(admin.ModelAdmin):
     list_display = ("title","course","is_preview",)
     # list_editable = ['is_preview']

admin.site.register(Course,CourseAdmin)
admin.site.register(Video,AdminVideo)
