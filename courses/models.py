from django.db import models
from django.utils.text import slugify
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
    resource = models.FileField(upload_to = "course/resource")
    length = models.IntegerField(null=False)

    def __str__(self):
        return self.name
   
    def save(self,*args, **kwargs):
         if self.slug:
              self.slug = slugify(self.name)
         return super().save(*args, **kwargs)
     
     
class CourseProperty(models.Model):
    description  = models.CharField(max_length = 100 , null = False)
    course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)

    class Meta : 
        abstract = True


class Tag(CourseProperty):
    pass
    
class Prerequisite(CourseProperty):
    pass

class Learning(CourseProperty):
    pass




#Video
class Video(models.Model):
    title  = models.CharField(max_length = 100 , null = False)
    video_description = models.CharField(max_length = 500 , null = True)
    course = models.ForeignKey(Course , null = False , on_delete=models.CASCADE)
    serial_number = models.IntegerField(null=False,unique=True)
    video_id = models.CharField(max_length = 100 , null = False)
    is_preview = models.BooleanField(default = False)

    def __str__(self):
        return f'course name: ({self.course}) --> video-title: {self.title}' 

    