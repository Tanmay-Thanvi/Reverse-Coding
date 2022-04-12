from django.db import models
from accounts.models import Profile
from django.contrib.auth.models import User
# Create your models here.
class question(models.Model):
    question = models.CharField(max_length=500)
    questiondesc = models.TextField(null=True,blank=True)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return self.question

class riddle(models.Model):
    riddle = models.CharField(max_length=500)
    riddledesc = models.TextField(null=True,blank=True)
    answer = models.CharField(max_length=200)

    def __str__(self):
        return self.riddle

class response(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    queid = models.ForeignKey(question,on_delete=models.CASCADE,default=None)
    response1 = models.CharField(max_length=200)
    response2 = models.CharField(max_length=200)
    r1_time = models.DateTimeField(null=True)
    r2_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.username+f' ({self.response1})'+f' ({self.response2})'

class userlist(models.Model):
    user= models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    unattemptedlist = models.TextField()
    attemptedlist = models.TextField(null=True,blank=True)
    correctlist = models.TextField(null=True,blank=True)
    attemptsleft = models.IntegerField(default=2) 
    markingscheme = models.CharField(max_length=100,default='4,2')

    def __str__(self):
        return self.user.username