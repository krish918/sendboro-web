from django.db import models

class User(models.Model):
    userid = models.AutoField(null=False, unique=True, primary_key=True)
    dialcode = models.CharField(null=False, max_length=8)
    phone = models.BigIntegerField(null=False)
    countrycode = models.CharField(max_length=4, default=None)
    username = models.CharField(null=True, blank=False, max_length=16, default=None, unique=True)
    fullname = models.CharField(null=True, blank=False, max_length=255, default=None)
    account_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True, default=None)
    
    unique_together = ("dialcode","phone")
    
    def __str__(self):
        return self.userid
    
class Session(models.Model):
    sessionid = models.AutoField(null=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uastring = models.CharField(null=False, max_length=512)
    ipaddress = models.CharField(null=False, max_length=16)
    active = models.BooleanField(default=True, null=False)
    start_ts = models.DateTimeField(auto_now_add=True)
    end_ts = models.DateTimeField(auto_now=True, default=None)
    
    def __str__(self):
        return self.sessionid
    
class UserMobileDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phoneagent = models.CharField(max_length=512, null=False, blank=False)
    ts = models.DateTimeField(auto_now_add=True)
    