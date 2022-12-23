from django.contrib import admin
from .models import Course,Video,SectionVideo,Assessment,SubmittedAssessment,Mark
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

class CourseAssessmentAdmin(admin.TabularInline):
    model = Assessment
    extra = 0
    
class CourseSubmittedAssessmentAdmin(admin.TabularInline):
    model = SubmittedAssessment
    extra = 0
class CourseMarkAdmin(admin.TabularInline):
    model = Mark
    extra = 0



# class LearningAdmin(admin.TabularInline):
#     model = Learning
#     extra = 1

# class PrerequisiteAdmin(admin.TabularInline):
#     model = Prerequisite 
#     extra = 1
    
class CourseAdmin(admin.ModelAdmin):
    inlines = [ SectionVideoAdmin ,CourseVideoAdmin,CourseAssessmentAdmin]
    prepopulated_fields = {"slug": ("name",)}  # new
    list_display = ("name","price","discount","active", "instructor")
    search_fields = ['name']
    
class SectionVideoAdminModel(admin.ModelAdmin):
    list_display = ["name","course"] 
    prepopulated_fields = {"slug": ("name",)}  # new
    
  

class AdminVideo(admin.ModelAdmin):
     list_display = ("title","course","is_preview",)
     # list_editable = ['is_preview']
    

class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title','course','maximum_number')
    search_fields = ['title']
 
    
class SubmittedAssessmentAdmin(admin.ModelAdmin):
    list_display = ('course','student_user','assessment')
    search_fields = ['course']
 
class MarkAdmin(admin.ModelAdmin):
    list_display = ('assessment','student_user','student_submitted_assessment')
    search_fields = ['assessment']
 
    



admin.site.register(Course,CourseAdmin)
admin.site.register(Video)
admin.site.register(SectionVideo,SectionVideoAdminModel)
admin.site.register(Assessment,AssessmentAdmin)
admin.site.register(SubmittedAssessment,SubmittedAssessmentAdmin)
admin.site.register(Mark,MarkAdmin)