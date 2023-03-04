from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
from accounts.models import UserProfile,Account
import uuid
from mptt.models import MPTTModel, TreeForeignKey
# from taggit.managers import TaggableManager# Create your models here.

class Category(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    slug = models.SlugField(allow_unicode=True,max_length=100,unique=True)
    description =models.TextField(max_length=300,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add = True) 
    modified_at = models.DateTimeField(auto_now = True)     

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return  self.name
    
    
    def save(self,*args, **kwargs):
         if self.slug:
              self.slug = slugify(self.name ,allow_unicode=True)
         return super().save(*args, **kwargs)


class Course(models.Model):
    instructor = models.ForeignKey(UserProfile,on_delete=models.CASCADE) 
    name = models.CharField(max_length = 50 , null = False,unique = True)
    slug = models.CharField(max_length = 50 , null = False , unique = True)
    description = models.CharField(max_length = 700 , null = True)
    
    categories =models.ForeignKey(Category, on_delete=models.CASCADE )
    
    price = models.IntegerField(null=False,default=0)
    discount = models.IntegerField(null=False , default = 0) 
    
    active = models.BooleanField(default = False)
    thumbnail = models.ImageField( upload_to = "course/thumbnail") 
    
    created_at = models.DateTimeField(auto_now_add = True) 
    modified_at = models.DateTimeField(auto_now = True) 
    
    resource = models.FileField(upload_to = "course/resource",null=True,blank=True)
    length = models.IntegerField(null=False,default=0)
    
    tags = TaggableManager()
    prerequisite = models.CharField(max_length = 50 , null = True, blank=True,default="No need ")
    learning = models.CharField(max_length = 50 , null = False) 
    top_course = models.BooleanField(default=False)

    def __str__(self):
        return self.name
   
    def save(self,*args, **kwargs):
         if self.slug:
              self.slug = slugify(self.name ,allow_unicode=True)
         return super().save(*args, **kwargs)
     
     
# class CourseProperty(models.Model):
#     description  = models.CharField(max_length = 100 , null = False)
#     course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)

#     class Meta : 
#         abstract = True


# # class Tag(CourseProperty):
# #     pass
    
# class Prerequisite(CourseProperty):
#     pass

# class Learning(CourseProperty):
#     pass
class SectionVideo(models.Model):
    course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)
    name = models.CharField(max_length = 50 , null = False)
    slug = models.CharField(max_length = 50 , null = False )
    serial_number = models.IntegerField(null=False)
    
    def save(self,*args, **kwargs):
         if self.slug:
              self.slug = slugify(self.name)
         return super().save(*args, **kwargs)
     
    def __str__(self):
        return self.name
     


#Video
class Video(models.Model):
    section_video = models.ForeignKey(SectionVideo , null = False , on_delete = models.CASCADE)
    course = models.ForeignKey(Course , null = False , on_delete = models.CASCADE)
    title  = models.CharField(max_length = 100 , null = False)
    video_description = models.CharField(max_length = 500 , null = True)
    serial_number = models.IntegerField(null=False)
    video_id = models.CharField(max_length = 100 , null = False)
    resource = models.CharField( max_length=200,null=True,blank=True)
    resource_title = models.CharField(max_length=100,null=True,blank=True)
    is_preview = models.BooleanField(default = False)
    video_unique_id = models.CharField(max_length=100, blank=True, unique=True, default=uuid.uuid4)

    
    
    # def __init__(self):
    #      super(Video, self).__init__()
    #      self.video_unique_id = str(uuid.uuid4())
    # def __unicode__(self):
    #     return self.title
    

    def __str__(self):
        return f'course name: ({self.section_video.course}) --> section name: ({self.section_video}) --> video-title: {self.title}' 


class EnrolledCourse(models.Model):
     user = models.ForeignKey(Account, on_delete=models.CASCADE)
     course = models.ForeignKey(Course, on_delete=models.CASCADE)
     enrolled = models.BooleanField(default=False)
     created_at = models.DateTimeField(  auto_now_add=True)
     
     def __str__(self):
          return f'{self.user} course:{self.course} '
     

    
# Assessment
class Assessment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title  = models.CharField(max_length = 100 , null = False)
    resource = models.CharField( max_length=200,null=False,blank=False)
    resource_title = models.CharField(max_length=100,default="Assessment")
    maximum_number  = models.IntegerField(null=False) 
    created_at = models.DateTimeField(auto_now_add = True) 
    modified_at = models.DateTimeField(auto_now = True) 
    
    def __str__(self):
        return f'course: ({self.course}) title: ({self.title})'


class SubmittedAssessment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_user = models.ForeignKey(EnrolledCourse, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    resource = models.CharField( max_length=200,null=False,blank=False)
    resource_title = models.CharField(max_length=100,null=False,blank=False)
    obtained_mark = models.IntegerField(default = 0)
    feedback = models.CharField( max_length=200,null=True,blank=True) 
    created_at = models.DateTimeField(auto_now_add = True) 
    modified_at = models.DateTimeField(auto_now = True) 
    
    def __str__(self):
        return f'{self.student_user}'

    # obtained = models.IntegerField(default =0)
    
class Mark(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    student_user = models.ForeignKey(Account, on_delete=models.CASCADE)
    student_submitted_assessment = models.ForeignKey(SubmittedAssessment, on_delete=models.CASCADE)
    obtained_mark = models.IntegerField(default = 0)
    feedback = models.CharField( max_length=200,null=True,blank=True) 
    
    # def __str__(self):
    #     return self.assessment
     
     
