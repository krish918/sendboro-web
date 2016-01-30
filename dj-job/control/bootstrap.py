from common.models import *
from authmod.models import RawUser
from django.db.models import F
from common.sms import TextMessage
from django.db import IntegrityError, transaction
from common.utils.general import Random,UserTrace
from django.utils.decorators import method_decorator
import hashlib, uuid

class Borouser():
    
    def __init__(self,**kwargs):
        if 'user' in kwargs:
            self.udata = kwargs['user']
        if 'dialcode' in kwargs and 'phone' in kwargs:
            self.dialcode = kwargs['dialcode']
            self.phone = kwargs['phone']
        if 'countrycode' in kwargs:
            self.countrycode = kwargs['countrycode']
        if 'req' in kwargs:
            self.req = kwargs['req']
        
    def sendphrase(self, **kwargs):
        #phrase decoded back to string
        if 'msg' in kwargs:
            message = kwargs['msg']
        else:
            message = ("Hello! You tried signing up for Sendboro."+
                " Please use this code to proceed : ")     
        text = message+self.phrase.decode()
        sms = TextMessage(text,self.fullphone)
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
    
    def addraw(self, **kwargs):
        retry = False
        try:
            self.fullphone = self.dialcode + self.phone
            hash = self.createhash()
            if 'resend' in kwargs:
                raise IntegrityError
            trace = UserTrace(self.req)
            ip = trace.getIp()
            ua = trace.getUastring()
        
            ru = RawUser(phone_no=self.fullphone, vericode=hash,
                             ipaddress=ip, uastring=ua)
            ru.save()
        except IntegrityError:
             RawUser.objects.filter(phone_no=self.fullphone).update(vericode=hash,
                                                                 attempt=F('attempt')+1)
             retry = True
        except:
             raise
        
        #self.sendphrase()    
        return {
                    'dialcode'   : self.dialcode,
                    'phone'      : self.phone,
                    'countrycode': self.countrycode,
                    'retry'      : retry
                }
        
        
    def attemptlogin(self):
        self.fullphone = self.udata.dialcode+str(self.udata.phone)
        hash = self.createhash()
        self.udata.vericode = hash
        self.udata.save()
        #self.sendphrase(msg = "Your Sendboro login code: ");
        return {
                'user' : self.udata,
                'return' : True
                }
        