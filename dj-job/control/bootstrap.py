from common.models import *
from common.sms import TextMessage
from django.db import IntegrityError, transaction
from common.utils.general import Random,UserTrace
from django.utils.decorators import method_decorator
import hashlib, uuid

class Borouser():
    countrycode = None
    phone = None
    username = None
    phrase = None
    fullname = None
    uid = None
    req = None
    
    def __init__(self,**kwargs):
        if 0 < len(kwargs):
            self.countrycode = kwargs['cc']
            self.phone = kwargs['phone']
            self.req = kwargs['req']
        
    def sendphrase(self):
        #phrase decoded back to string
        text = ("Please use this code as your "+ 
                    "password to login next time on sendboro: ")+self.phrase.decode()
        full_phone = self.countrycode+self.phone
        sms = TextMessage(text,full_phone)
        sms.send()
        
    @method_decorator(transaction.atomic)   
    def create(self):
        #encoding into byte object as hashing is done only on bytes
        hash = self.createhash()
        try:
            usr = User(countrycode=self.countrycode,phone=self.phone,phash=hash)
            usr.save()
            self.uid = usr.userid
            self.initsession()
        except:
            raise
        self.sendphrase()
        
    def createhash(self, *args):
        if 0 < len(args):
            phrase = args[0].encode('utf-8')
        else:
            self.phrase = str(Random(1,5,5).create()).encode('utf-8')
            phrase = self.phrase
            
        #byte encoded salt
        if 1 < len(args):
            salt = args[1].encode('utf-8')
        else:
            salt = uuid.uuid4().hex.encode('utf-8')
            
        hash = hashlib.sha512(phrase + salt).hexdigest()
        
        #converted back to strings explicitly to accord format specifier
        stored_hash = 's5$%s$%s' % (str(salt),str(hash))
        return stored_hash
        
    def initsession(self):
        
        #getting ip and uastring
        trace = UserTrace(self.req)
        ip = trace.getIp()
        ua = trace.getUastring()
        
        #creating user object for inserting into session relation
        user = User.objects.get(pk=self.uid)
                                
        #inserting in session relation
        sess = user.session_set.create(uastring=ua, ipaddress=ip)
        sid = sess.sessionid
        
        # claro viejo session
        self.req.session.clear()
        
        #setting session objects
        self.req.session['user_id'] = self.uid
        self.req.session['session_id'] = sid
        