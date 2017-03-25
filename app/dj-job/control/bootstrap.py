from common.models import User as Usermodel
from authmod.models import RawUser, CodeHash
from django.db.models import F
from django.db import IntegrityError, transaction
from common.utils.general import Random,UserTrace,Helper
from django.utils.decorators import method_decorator
from common.base.constant import Const
from common.base import session
from common.base.user import User

class Rawuser(User):
    
    def __init__(self, fullphone):
        super(Rawuser,self).__init__(fullphone)
        
    @method_decorator(transaction.atomic)    
    def Add(self):
        reattempt = False
        trace = UserTrace(User.request)
        ip = trace.getIp()
        ua = trace.getUastring()
        try:
            with transaction.atomic():
                ru = RawUser(phone_no=self.fullphone, ipaddress=ip, uastring=ua)
                ru.save()
        except IntegrityError:
             RawUser.objects.filter(phone_no=self.fullphone).update(attempt=F('attempt')+1)
             reattempt = True
        except:
             raise
        self.SendVeriCode()
        
    def SendVeriCode(self):
        super(Rawuser,self).SendVeriCode()
        msg = "Hello! You tried signing up for Sendboro. Please use this code to proceed: "
        msg += self.phrase+". "+self.linktext
        self.SendText(msg)
        

class Borouser(User):
    
    def __init__(self, fullphone):
        super(Borouser,self).__init__(fullphone)
    
    @method_decorator(transaction.atomic)   
    def Add(self):
        self.user = Usermodel(dialcode=self.dialcode,phone=self.phone,countrycode=self.countrycode)
        self.user.save()
        self.StartSession()
    
    def StartSession(self):
        sesn = session.Session(User.request, self.user)
        sesn.Create()
        
    def SendVeriCode(self):
        super(Borouser,self).SendVeriCode()
        msg = "Your Sendboro login code is: "+self.phrase+". "+self.linktext
        return self.SendText(msg)
        