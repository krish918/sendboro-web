from common.models import User, Session
from authmod.models import RawUser, CodeHash
from django.db.models import F
from common.sms import TextMessage
from django.db import IntegrityError, transaction
from common.utils.general import Random,UserTrace,Helper
from django.utils.decorators import method_decorator
from common.base.constant import Const
import hashlib, uuid

class Borouser():
    
    def __init__(self,**kwargs):
        if 'dialcode' in kwargs and 'phone' in kwargs:
            self.dialcode = kwargs['dialcode']
            self.phone = kwargs['phone']
            self.fullphone = self.dialcode + str(self.phone)
        if 'countrycode' in kwargs:
            self.countrycode = kwargs['countrycode']
        if 'req' in kwargs:
            self.req = kwargs['req']
        
    def sendphrase(self, msg):
        #phrase decoded back to string
        sms = TextMessage(msg, self.fullphone)
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
    
    @method_decorator(transaction.atomic)
    def addraw(self, **kwargs):
        reattempt = False
        trace = UserTrace(self.req)
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
        
        self.sendvericode(Const.SIGNUP)
        return {
                    'dialcode'   : self.dialcode,
                    'phone'      : self.phone,
                    'reattempted': reattempt,
                }
        
    def sendvericode(self, mode):
        generated_hash = self.createhash()
        hash_entity = CodeHash(hash=generated_hash)
        hash_entity.save()
        hashid = hash_entity.id
        self.req.session['hashid'] = hashid
        link = Helper().getHostString(self.req)+'/'+str(hashid)+'/'+self.phrase.decode()
        linktext = "You may also tap on this link: "+link
        if mode == Const.SIGNUP:
            msg = "Hello! You tried signing up for Sendboro. Please use this code to proceed: "
            msg += self.phrase.decode()+". "+linktext
        elif mode == Const.SIGNIN:
            msg = "Your Sendboro login code is: "+self.phrase.decode()+". "+linktext
            msg += ". DO NOT visit this link if it wasn't requested by you!"
        #self.sendphrase(msg)        
        
    def attemptlogin(self, **kwargs):
        self.sendvericode(Const.SIGNIN)
        
        return {
                'dialcode': self.dialcode,
                'phone'  : self.phone,
                'return' : True,
                }
        