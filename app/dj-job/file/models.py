from django.db import models
from common.models import User
from common.utils.general import Helper

class File(models.Model):
    fileid = models.AutoField(null=False, unique=True, primary_key=True)
    filename = models.CharField(null=False, max_length=255)
    path = models.FileField(upload_to=Helper.getFilePath, null=False, blank=False, max_length=512)
    size = models.CharField(null=False, max_length=10)
    type = models.CharField(max_length=255, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    recievers = models.ManyToManyField(User, related_name='Receiver', through='Delivery')
    shorturl = models.CharField(max_length=8, null=True, unique=True)
    sent_ts = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.fileid
    
class Delivery(models.Model):
    
    dlvry_status = (
                  ('0', 'Reached Server'),
                  ('1', 'Seen'),
                  ('2', 'Downloaded'),
                  ('3', 'Directlink'),
                  ('4', 'Both'),
            )
    
    file = models.ForeignKey(File)
    user = models.ForeignKey(User)
    status = models.CharField(max_length=1, default='0', choices=dlvry_status)
    update_ts = models.DateTimeField(auto_now=True)
    
class BlindDelivery(models.Model):
    
    dlvry_status = (
                  ('0', 'stored'),
                  ('1', 'moved'),
            )
    
    file = models.ForeignKey(File)
    phone = models.CharField(null=False, blank=False, max_length=100)
    status = models.CharField(max_length=1, default='0', choices=dlvry_status)
    update_ts = models.DateTimeField(auto_now=True)
    
class DirectUnsignedView(models.Model):
    
    file = models.ForeignKey(File)
    viewer_ip = models.CharField(max_length=16)
    viewer_ua = models.CharField(max_length=512)
    ts = models.DateTimeField(auto_now_add=True)
    