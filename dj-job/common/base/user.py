from abc import ABCMeta, abstractmethod
from authmod.models import CodeHash
from common.utils.general import Helper, Random, UserTrace
from com.sms import TextMessage
from common.base.boroexception import BoroException
from common.base.constant import Const
import hashlib, uuid

class classproperty(property):
    def __get__(self,cls,owner):
        return self.fget.__get__(None,owner)()

class User(metaclass = ABCMeta):
    """ Abstract Class to implement when defining a user """
    
    __request = None
    
    @classproperty
    @classmethod
    def request(cls):
        return cls.__request
    
    @request.setter
    @classmethod
    def request(cls, value):
        cls.__request = value
        
    ''' request must be set before instantiating class '''    
    def __new__(cls, *args, **kwargs):
        if cls.request is None:
            raise BoroException("request not set. Can't instantiate User",Const.INSTANCE_ERROR)
        return super(User,cls).__new__(cls)
        
    def __init__(self, phone):
        self.fullphone = phone
        
            
    ''' Implementing overloaded constructors '''       
    @classmethod
    def CreateWithPhone(cls, dc, ph):
        obj = cls(dc+ph)
        obj.dialcode = dc
        obj.phone = ph
        return obj
    
    @classmethod
    def CreateWithFullCredential(cls,dc,ph,cc):
        obj = cls.CreateWithPhone(dc,ph)
        obj.countrycode = cc
        return obj 
    
    @classmethod
    def CreateWithUser(cls, userObj):
        obj = cls(userObj.dialcode+str(userObj.phone))
        obj.user = userObj
        obj.dialcode = userObj.dialcode
        obj.phone = str(userObj.phone)
        return obj       
            
    @abstractmethod
    def Add(self):
        pass
    
    @abstractmethod
    def SendVeriCode(self):
        if 'hashid' in User.request.session and 'phrase' in User.request.session:
            self.ReuseVericode()
        else:
            self.GenerateVericode()
    
    def ReuseVericode(self):
        self.phrase = User.request.session['phrase']
        self.hashid = User.request.session['hashid']
        self.prepareText()
    
    def GenerateVericode(self):
        generated_hash, self.phrase = User.createhash()
        trace = UserTrace(User.request)
        hash_entity = CodeHash(hash=generated_hash,requestagent=trace.getUastring(),requestip=trace.getIp())
        hash_entity.save()
        User.request.session['hashid'] = self.hashid = hash_entity.id
        User.request.session['phrase'] = self.phrase
        self.prepareText()
        
    def prepareText(self):
        link = Helper.getHostString(User.request)+'/'+str(self.hashid)+'/'+self.phrase
        self.linktext = "You may also tap on this link: "+link
            
    @staticmethod
    def createhash(*args):
        if 0 < len(args):
            phrase = args[0].encode('utf-8')
        else:
            phrase = str(Random(Random.NUMERIC_CODE,5,5).create()).encode('utf-8')
            
        #byte encoded salt
        if 1 < len(args):
            salt = args[1].encode('utf-8')
        else:
            salt = uuid.uuid4().hex.encode('utf-8')
            
        hash = hashlib.sha512(phrase + salt).hexdigest()
        
        #converted back to strings explicitly to accord format specifier
        stored_hash = 's5$%s$%s' % (str(salt),str(hash))
        if len(args) > 0:
            return stored_hash
        return stored_hash, phrase.decode()
    
    def SendText(self, msg):
        #phrase decoded back to string
        sms = TextMessage(msg, self.fullphone)
        #sms.send()
    