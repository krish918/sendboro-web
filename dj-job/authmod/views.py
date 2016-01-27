from django.http import HttpResponse
from django.views.generic import View
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from authmod.models import RawUser
from django.db import IntegrityError, transaction
from common.models import User
from common.sms import TextMessage
from common.utils.general import Random, UserTrace
from control.bootstrap import Borouser
from common.models import User, Session
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
try:    
    from django.utils import simplejson
except:
    import simplejson
import re, sys, traceback
from common.base.boroexception import BoroException
from common.base.constant import Const

class SignonView(View):
    
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(SignonView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.response = {}
        self.dialcode = request.POST.get('dc',False)
        self.credential = request.POST.get('crdntl',False)
        self.countrycode = request.POST.get('cc',False)
        try:
           res = self.validateInput()
           if isinstance(res, User):
               acc = Account(res)
               self.response = acc.signin()
           else:
               bu = Borouser(dialcode=self.dialcode,phone=self.credential,req=request)
               acc = Account(bu)
               self.response = acc.signup()
               self.response['countrycode'] = self.countrycode
                  
        except BoroException as e:
            self.response = {'success' : False, 'errorcode' : e.code }
        except Exception as e:
            self.response = { 'success' : False,
                              'errorcode' : Const.AUTH_ERROR,
                              'message' : e.__str__()
                              }
            
        dump = simplejson.dumps(self.response)
        return HttpResponse(dump, content_type='application/json')
    
    def validateInput(self):
        dialCodeWithoutSpace = False
        
        patternUserName = r'^[a-zA-Z][a-zA-Z0-9\.]+$'
        patternAltCredent = r'[a-zA-Z]'
        patternDialCode = r'^\+[0-9]{1,8}$'
        patternPhone = r'[^0-9]'
        
        if self.credential is False:
            raise BoroException("No credential in request.",Const.INVALID_REQUEST)
        
        credential = self.credential.strip().replace(' ','')
        
        if self.dialcode is not False:
            dialCodeWithoutSpace = self.dialcode.strip().replace(' ','')
            countryCode = self.countrycode.strip()
            matchDialCode = re.search(patternDialCode, dialCodeWithoutSpace)
            
        matchAltCredent = re.search(patternAltCredent, credential)
        matchUserName = re.search(patternUserName, credential)
        
        if matchAltCredent and matchUserName:
            try:
                user = User.objects.get(username=credential)
                return user
            except:
                raise BoroException("",Const.USERNAME_NOTEXIST)
            
        elif matchAltCredent and not matchUserName:
            raise BoroException("", Const.INVALID_USERNAME)
        elif dialCodeWithoutSpace is False or not matchDialCode\
         or len(countryCode) == 0:
            raise BoroException("",Const.INVALID_DIALCODE)
        else:
            matchNotPhone = re.search(patternPhone, credential)
            if matchNotPhone or len(credential) == 0 or len(dialCodeWithoutSpace+credential) > 16:
                raise BoroException("", Const.INVALID_PHONE)
            try:
                user = User.objects.get(phone=credential,countrycode=dialCodeWithoutSpace)
                return user
            except:
                pass
        self.credential = credential
        self.dialcode = dialCodeWithoutSpace
        return False
            
        
class SigninView(View):
    
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(SigninView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.phone = request.POST['phone']
        self.ac = request.POST['ac']
        self.code = request.POST['code']
        self.data = {}
        
        try:
            usr = User.objects.get(phone=self.phone,countrycode=self.ac)
            hash = usr.phash
            salt = (hash.split('$')[1])[2:-1]
            givenhash = Borouser().createhash(self.code,salt)
            if hash == givenhash:
                trace = UserTrace(request)
                ip = trace.getIp()
                ua = trace.getUastring()
                
                sess = usr.session_set.create(uastring=ua, ipaddress=ip)
                sid = sess.sessionid
        
                # claro viejo session
                request.session.clear()
        
                #setting session objects
                request.session['user_id'] = usr.userid
                request.session['session_id'] = sid
                
                self.data['success'] = 1
                
            else:
                self.data['error'] = 2
                 
        except ObjectDoesNotExist:
            self.data['error'] = 1
        except:
            self.data['error'] = traceback.format_exc()
            
        dump = simplejson.dumps(self.data)
        return HttpResponse(dump, content_type="application/json")
        
class Account:
        
    def __init__(self, userObj):
        if isinstance(userObj, User) or isinstance(userObj, Borouser):
            self.user = userObj
        else:
            raise Exception("Invalid User Object")
        
    def signup(self):
        response = self.user.addraw()
        return response
    
    def siginin(self):
        borouser = Borouser()
        hash = borouser.createhash(); 
        try:
            self.user.objects.filter(phone_no=full_phone).update(vericode=hash)
            borouser.sendphrase(msg="Your Sendboro login code : ");
        except:
            raise Exception("Couldn't Update hash or send text")
        
        return {
                'userid' : self.usr.userid,
                'return' : True,
                'success': True
                }
        
        
        
        
class VerifyCodeView(View):
    code = None
    areacode = None
    phone = None

    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(VerifyCodeView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        datadump = {}
        self.code = request.POST['code']
        self.areacode = request.POST['ac']
        self.phone = request.POST['ph']
        full_phone = self.areacode + self.phone
        
        try:
            get_rawuser = RawUser.objects.get(phone_no=full_phone, vericode=self.code)
            
            #sending request as parameter to initialize session handling
            self.createacc(request)
            
            datadump['success'] = 1
        except ObjectDoesNotExist:
            datadump['error'] = 1
        except MultipleObjectsReturned:
            datadump['error'] = 2
        except:
            datadump['error'] = 3
        
        data = simplejson.dumps(datadump)
        return HttpResponse(data, content_type='application/json')
        
    def createacc(self,request):
        try:
            bu = Borouser(cc=self.areacode, phone=self.phone, req=request)
            bu.create()
        except:
            raise
        