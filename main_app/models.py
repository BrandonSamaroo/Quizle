from email.policy import default
from optparse import Option
from unicodedata import name
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=30)

class Quiz(models.Model):
    name = models.CharField(max_length=30)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to ='images/quizes/', default='images/quizes/default_quiz.jpg')
    topic = models.ManyToManyField(Topic)

class Score(models.Model):
    score = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    answer = models.CharField(max_length=30)
    option1 = models.CharField(max_length=30)
    option2 = models.CharField(max_length=30)
    option3 = models.CharField(max_length=30)
    option4 = models.CharField(max_length=30)

class UserExtras(models.Model):
    profilePic = models.ImageField(upload_to ='images/profiles/', default='images/profiles/default_profile.jpg')
    followedTopics = models.ManyToManyField(Topic)
    user = models.OneToOneField(User, on_delete=models.CASCADE)



