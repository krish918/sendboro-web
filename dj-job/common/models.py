from django.db import models

class User(models.Model):
    userid = models.AutoField(null=False, unique=True, primary_key=True)
    countrycode = models.CharField(null=False, max_length=4)
    phone = models.BigIntegerField(null=False, unique=True)
    username = models.CharField(null=True, blank=False, max_length=16, default=None, unique=True)
    phash = models.CharField(null=False, blank=False, max_length=512)
    fullname = models.CharField(null=True, blank=False, max_length=255, default=None)
    account_ts = models.DateTimeField(auto_now_add=True)
    update_ts = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.userid
    
class Session(models.Model):
    sessionid = models.AutoField(null=False, unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    uastring = models.CharField(null=False, max_length=512)
    ipaddress = models.CharField(null=False, max_length=16)
    active = models.BooleanField(default=True)
    ts = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.sessionid
    