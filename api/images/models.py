from django.db import models
from django.conf import settings

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField('Email Address', unique=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

class Patient(models.Model):
    
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=False)
    email = models.EmailField(blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Study(models.Model):
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('title', 'patient',)
    
class Image(models.Model):
    
    name = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    study = models.ForeignKey(Study, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = (('name', 'study',), ('file_name', 'study',),)
    
class ImageComment(models.Model):
    
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    
    