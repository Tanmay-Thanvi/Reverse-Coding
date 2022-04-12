from django.db import models
from django.contrib.auth.models import User


# Create your models here.class Profile(models.Model):
# Create your models here.
class Profile(models.Model):
   user=models.OneToOneField(User,on_delete=models.CASCADE)
   has_started = models.BooleanField(default=False)
   is_notallowed = models.BooleanField(default=True)
   StartTime = models.DateTimeField(null=True,blank=True)
   ExpLgtTime = models.DateTimeField(null=True,blank=True)
   CompTime = models.DateTimeField(null=True,blank=True)
   Timetaken = models.TextField(null=True,blank=True)
   score = models.IntegerField(default=0)
   zone = models.CharField(max_length=100,default="Red")
   zone_activate = models.BooleanField(default=False)
   riddle_activate = models.BooleanField(default=False)
   
   def __str__(self):
    return self.user.username