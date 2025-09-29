from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    name = models.CharField(max_length=200)
    participants = models.ManyToManyField(User, related_name='participant', blank=True)
    updated = models.DateTimeField(auto_now=True) #auto_now takes timestamp when save is clicked
    created = models.DateTimeField(auto_now_add=True)#auto_now_add take timestamp only once the instance is created

    class Meta:
        ordering = ['-updated','-created']
    
    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  #CASCADE deletes permanently
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #or models.SET_NULL
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]