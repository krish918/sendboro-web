# for performing account related activities

from control.bootstrap import Borouser
from authmod.models import CodeHash
from common.base.constant import Const
import re

class Account:
        
    # Account object can be constructed even if identity of user is unknown     
    def __init__(self, *args):
        if len(args) != 0 and isinstance(args[0], Borouser):
            self.user = args[0]
        
    def signup(self):
        response = self.user.addraw()
        response['success'] = True
        return response
    
    def signin(self, loginName):
        response = self.user.attemptlogin()
        if loginName is not None:
            response['uname'] = loginName
            #sending obfuscated phone number
            response['phone'] = re.sub(r'(?<=[0-9])[0-9](?=[0-9]{3,3})','*',str(response['phone']))
        response['success'] = True 
        return response
    
    def pollChallenge(self,hashid):
        try:
            hc = CodeHash.objects.get(id=hashid, challenge__gt=0)
            challenge = str(hc.challenge)
            orighash = hc.hash
            givenhash = Borouser().createhash(challenge, (orighash.split('$')[1])[2:-1])
            if givenhash == orighash:
                return Const.VALID_CODE
            else:
                hc.challenge = 0
                hc.save()
                return Const.INVALID_CODE
        except CodeHash.DoesNotExist:
            return Const.EMPTY_POLL
            