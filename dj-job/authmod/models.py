from django.db import models
from django.core.validators import RegexValidator

class RawUser(models.Model):
    phone_no = models.CharField(max_length=16, unique=True)
    attempt = models.IntegerField(default=1)
    uastring = models.CharField(max_length=512, default=None, null=True)
    ipaddress = models.CharField(max_length=16, default=None, null=True)
    ts = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return self.phone_no
    
class CodeHash(models.Model):
    hash = models.CharField(max_length=255, null=False, blank=False)
    challenge = models.IntegerField(default=0, max_length=7, null=False,blank=False)
    responseagent = models.CharField(max_length=512, default=None, null=True, blank=False)
    requestip = models.CharField(null=True, default=None,blank=False, max_length=16)
    requestagent = models.CharField(max_length=512, default=None, null=True, blank=False)
    resolve_status = models.BooleanField(default=False, null=False)
    mitigate = models.BooleanField(default=False, null=False)
    ts = models.DateTimeField(auto_now_add=True, null=False)
    
