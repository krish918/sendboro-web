from django.db import models
from common.models import User
import uuid,os
from django_resized import ResizedImageField

# Create your models here.
class Picture(models.Model):
    
    target ='photo/user/%Y/%m/%d'
    picid = models.AutoField(null=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    large = models.ImageField(upload_to=target)
    med = ResizedImageField(size=[150,150], crop=['middle','center'], upload_to=target)
    small = ResizedImageField(size=[70,70],crop=['middle', 'center'],upload_to=target)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.picid

        
        
        