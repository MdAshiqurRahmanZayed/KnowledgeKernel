from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager
import uuid
# from taggit.managers import TaggableManager# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length = 50 , null = False,unique = True)
    slug = models.CharField(max_length = 50 , null = False , unique = True)
    description = models.CharField(max_length = 500 , null = True)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False , default = 0) 
    active = models.BooleanField(default = False)
    thumbnail = models.ImageField(upload_to = "course/thumbnail") 
    date = models.DateTimeField(auto_now_add= True) 
    resource = models.FileField(upload_to = "course/resource",null=True,blank=True)
    length = models.IntegerField(null=False)
    tags = TaggableManager()
    prerequisite = models.CharField(max_length = 50 , null = False)
    learning = models.CharField(max_length = 50 , null = False)

    def __str__(self):
        return self.name
   
    def save(self,*args, **kwargs):
         if self.slug:
              self.slug = slugify(self.name)
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

    