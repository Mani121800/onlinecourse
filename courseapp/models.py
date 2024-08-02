from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
  
    flag = models.IntegerField() 
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # flag = models.IntegerField(choices=FLAG_CHOICES, default=0)
    # link = models.URLField(blank=True, null=True)
    batch_number = models.IntegerField(default=0)  # New field for batch number

    def __str__(self):
        return self.user.username
    

    
from django.db import models

class Course(models.Model):
    title = models.CharField(max_length=200)
    batch_number = models.IntegerField()  # Add batch number field

    def __str__(self):
        return self.title

class Video(models.Model):
    course = models.ForeignKey(Course, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    video_url = models.FileField(upload_to='videos/')
    order = models.IntegerField()
    Description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
