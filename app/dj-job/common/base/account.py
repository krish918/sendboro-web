# for performing account related activities

from control.bootstrap import Borouser
from authmod.models import CodeHash
from common.base.constant import Const
import re

class Account:
           
    def __init__(self, user):
        if isinstance(user, Borouser) is False:
            raise BoroException("Can't init Account instance", Const.INSTANCE_ERROR)
        self.user = user
        
    def Create(self):
        self.user.Add()
        
    def Signin(self):
        self.user.StartSession()
    
    def AttemptLogin(self, loginName):
        vericode_res = self.user.SendVeriCode()
        response = {'dialcode':self.user.dialcode,
                         'phone':self.user.phone,
                         'success':True,
                         'return':True,
                         'vericode' : vericode_res, 
                         }        
        if loginName is not None:
            response['uname'] = loginName
            #sending obfuscated phone number
            response['phone'] = re.sub(r'(?<=[0-9])[0-9](?=[0-9]{3,3})','*',str(response['phone']))
        return response
    
    @staticmethod
    def PollChallenge(hashid):
        try:
            hc = CodeHash.objects.get(id=hashid, challenge__gt=0)
            challenge = str(hc.challenge)
            orighash = hc.hash
            givenhash = Borouser.createhash(challenge, (orighash.split('$')[1])[2:-1])
            if givenhash == orighash:
                hc.resolve_status = True
                hc.save()
                return Const.VALID_CODE
            else:
                hc.challenge = 0
                hc.save()
                return Const.INVALID_CODE
        except CodeHash.DoesNotExist:
            return Const.EMPTY_POLL
        