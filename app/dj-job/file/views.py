from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.views.generic import View
from common.utils.decorator import LoginRequired
from common.utils.general import UserTrace
from django.db import transaction
from common.models import User
from file.models import Delivery, File, BlindDelivery, DirectUnsignedView
from django.utils.decorators import method_decorator
from django.utils.encoding import smart_text, smart_bytes
import simplejson, traceback
from common.utils.general import Helper
from com.sms import TextMessage
from wsgiref.util import FileWrapper
from django.db import connection
from django.core.urlresolvers import resolve, Resolver404
from urllib.parse import urlparse
import os, mimetypes
from sendboro.settings import MEDIA_ROOT


class PushView(View):
    
    def __init__(self):
        self.res = {}
        self.recipient = None
        self.blind = False
        self.type = None
    
    @method_decorator(LoginRequired())
    def post(self, request, *args, **kwargs):
        
        self.host = request.META.get('HTTP_HOST',
                                request.META.get('SERVER_NAME',False))
        if not self.host:
            self.host = 'localhost:8080'
        
        self.recipient = request.POST['receiver']
        self.blind = request.POST.get('blind', False)
        self.user = request.session['user_id']
        self.file = request.FILES['file']
        self.name = self.file.name
        self.size = self.file.size
        self.type = self.file.content_type
        
        if self.size > 429916160:
            self.res['error'] = 1
        else:
            self.saveFile()
            
        data = simplejson.dumps(self.res)
        return HttpResponse(data, content_type='application/json')
    
    def saveFile(self):
        try:
            with transaction.atomic():
                u = User.objects.get(pk=self.user)
                f = u.file_set.create(filename=self.name,path=self.file,size=self.size,type=self.type)
                
                if self.blind is False:
                    receiver = User.objects.get(pk=self.recipient)
                    d = Delivery.objects.create(file=f, user=receiver)
                    target_phone = str(str(receiver.dialcode)+str(receiver.phone))
                else:
                    d = BlindDelivery.objects.create(file=f,phone=self.recipient)
                    target_phone = self.recipient
                    
                if u.username:
                    self.sender = str(u.username)
                else:
                    self.sender = str(u.dialcode)+str(u.phone)
                    
                self.sendsms(target_phone,f.fileid,f.path.url);
                
                self.res['success'] = 1
        except:
            self.res['error'] = traceback.format_exc()
            raise
            
    def sendsms(self, phone,fid, url):
        type = Helper().getFormattedType(self.type,self.name,True)
        texturl = 'http://'+str(self.host)+'/file/direct?id='+str(fid)+'&url='+str(url)
        
        msg = ("Hi! %s has sent you a %s file via sendboro."\
               +" Please sign up for sendboro to receive the file."\
               +" Or simply visit this URL to see the file: %s") % (self.sender,type,texturl)
                 
        sms = TextMessage(msg, phone)
        sms.send()
        
class DownloadView(View):
    
    def post(self, request, *args, **kwargs):
        fid = request.POST['fileid']
        uid = request.session['user_id']
        
        file = File.objects.get(pk=fid)
        try:
            cursor = connection.cursor()
            cursor.execute('''UPDATE file_delivery SET 
                                    status = CASE 
                                                WHEN status='1' OR status='2' THEN '2' 
                                                WHEN status='3' THEN '4'
                                                ELSE '2' 
                                             END 
                                    WHERE file_id = %s AND user_id = %s''', [fid, uid])
        except:
            pass
            
        filepath = os.path.join(MEDIA_ROOT, str(file.path))
        
        type = mimetypes.guess_type(file.path.url)
        response = HttpResponse(FileWrapper(open(filepath, "rb")), content_type=type)
        response['Content-disposition'] = 'attachment; filename=%s' % str(file.filename)   
        return response
        
            
            
    
class ChangeStateView(View):
    
    def post(self,request,*args,**kwargs):
        uid = request.session['user_id']
        res = {}
        try:
             Delivery.objects.filter(user__userid=uid,status='0').update(status='1')
             res['success'] = 1
        except:
            res['error'] = traceback.format_exc()
        
        dump = simplejson.dumps(res)
        return HttpResponse(dump, content_type='application/json')
    
class DirectLinkView(View):
    
    def get(self,request,*args,**kwargs):
        fid = request.GET.get('id',False)
        uid = request.session.get('user_id', False)
        url_to_visit = request.GET.get('url', False)
        
        if not fid or not url_to_visit:
            return HttpResponseNotFound('Invalid Request')
        
        if uid:
            try:
                cursor = connection.cursor()
                cursor.execute('''UPDATE file_delivery SET 
                                    status = CASE 
                                                WHEN status='1' OR status='3' THEN '3' 
                                                WHEN status='2' THEN '4'
                                                ELSE '3' 
                                             END 
                                    WHERE file_id = %s AND user_id = %s''', [fid, uid])
            except:
                pass
        
        else:
            trace = UserTrace(request)
            ip = trace.getIp()
            ua = trace.getUastring()
            
            try:
                fileobj = File.objects.get(pk=fid)
                DirectUnsignedView.objects.create(file=fileobj,viewer_ip=ip,viewer_ua=ua)
            except:
                pass
        
            
        response = HttpResponseRedirect(url_to_visit)
        
        #try:
        #    resolve(urlparse(url_to_visit)[2])
        #except Resolver404:
        #    pass
            #return HttpResponseNotFound()
           
        return response
    
