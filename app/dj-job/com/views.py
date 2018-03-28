from django.shortcuts import render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST, require_GET
from common.base.constant import Const
from common.base.boroexception import BoroException
import plivo, plivoxml, simplejson, traceback
from django.http.response import HttpResponse
from com.call import VoiceCall
from com.sms import TextMessage
from django.views.decorators.csrf import csrf_exempt
from lxml import etree

''' view to generate an xml file to be requested by plivo
    for an automated reply to users if they call sendboro's number'''
class AutoReplyInXml(View):
    
    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(AutoReplyInXml, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        r = plivoxml.Response()
        
        body = u'''Hello and welcome to Send Borrow! We have received your service request. 
        Our consumer care executive will get in touch with you shortly. Thank you for choosing
        Send Borrow.'''
        
        params = {
                  'language': "en-US",
                  'voice': "WOMAN",
                  'loop': "1",
                  }
        
        r.addSpeak(body, **params)
        return HttpResponse(str(r), content_type='text/xml')
    
'''View to generate xml file to be requested
   by plivo to send the code as a voice call'''
class CodeSpeechInXml(View):
    
    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(CodeSpeechInXml, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        #r = plivoxml.Response()
        try:
            if kwargs['code'] is None:
                raise BoroException("Endpoint not valid", Const.GEN_ERROR)          
            
            # separating digits of code by space to let bot speak them separately  
            code = ""
            for digit in kwargs['code']:
                code = code + digit + ", "
                
            body = "Your send borrow verfication code is; " + str(code) + ". "
            
            res_root = etree.Element('Response')
            
            #adding speak elemnet in XML response
            res_speak = etree.Element('Speak', language="en-GB", voice="WOMAN", loop="0")
            res_speak.text = body
            res_root.append(res_speak)
            
            #url = "https://boro.ngrok.io/content/res/rec.mp3"
            #res_play = etree.Element('Play');
            #res_play.text = url
            #res_root.append(res_play)
            #params = {
             #         'language': "en-GB",
              #        'voice': "MAN",
               #       'loop': "0",
                #      }
            
            #r.addSpeak(body, **params)
            #print(r.to_xml())
        except:
            pass
        
        return HttpResponse(etree.tostring(res_root), content_type='text/xml')

''' View to probed by ajax poll for requesting
     a voice call to get the verification code'''    
class VoiceCallCode(View):
    
    def __init__(self):
        self.response = {}
    
    def post(self, request, *args, **kwargs):
        try:
            self.host = request.META.get('HTTP_HOST', 
                                     request.META.get('SERVER_NAME', False))
            if self.host is False:
                self.host = "sendboro.com"
                
            if request.is_secure() is True:
                self.protocol = "https"
            else:
                self.protocol = "http"
        
            self.code = request.session.get('phrase', False)
            self.phone = request.session.get('fullphone', False)
            if self.code is False or self.phone is False:
                raise BoroException("Session store is invalid.", Const.AUTH_ERROR)
            
            answer_url = self.protocol+"://"+self.host+"/com/api/voice/code/"+str(self.code)
            
            vc = VoiceCall(self.phone, str(answer_url))
            status = vc.call()
            self.response['success'] = True
            self.response['status'] = status
            
        except Exception as e:
            self.response = {
                             'success': False,
                             'error': Const.CALL_ERROR,
                             'message': str(e),
                             }
        
        dump = simplejson.dumps(self.response)
        return HttpResponse(dump, content_type="application/json")
        
class RecordActionView(View):
    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(RecordActionView, self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        root = etree.Element("ok")
        #record_length = request.GET.get("RecordingDuration", False)
        
        
        report = TextMessage("URL: "+request.POST.get("RecordUrl",False),"918755823631")
        report.send()
        
        return HttpResponse(etree.tostring(root), content_type="text/xml")
        
class RawCallView(View):
    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(RawCallView,self).dispatch(*args, **kwargs)
        
    def post(self, *args, **kwargs):
        self.response = {}
        try:
            phone = request.POST.get("phone", false)
            if phone is False:
                raise
            host = request.META.get('HTTP_HOST', 
                            request.META.get('SERVER_NAME', False))
            if host is False:
                host = "sendboro.com"
                
            if request.is_secure() is True:
                protocol = "https"
            else:
                protocol = "http"
        
            answer_url = protocol+"://"+host+"/com/api/rawcallrecord"
            
            vc = VoiceCall(phone, str(answer_url))
            status = vc.call()
        
            self.response['succes'] = True
        except:
            self.response['success'] = False
            
        res = simplejson.dumps(self.response)
        return HttpResponse(res, content_type="application/json")
        
class RawCallRecordView(View):
    @method_decorator(csrf_exempt)
    @method_decorator(require_POST)
    def dispatch(self, *args, **kwargs):
        return super(RawCallView,self).dispatch(*args, **kwargs)
    
    def post(self, request, *args, **kwargs):
    
        #getting action_url for call recording report
            
        host = request.META.get('HTTP_HOST', 
                            request.META.get('SERVER_NAME', False))
        if host is False:
            host = "sendboro.com"
                
        if request.is_secure() is True:
            protocol = "https"
        else:
            protocol = "http"
                
        action_url = protocol+"://"+host+"/com/api/record" 
        res_root = etree.Element('Response')
        
        speak_elem = etree.Element('Speak')
        speak_elem.text = "This is an automated call from send borrow bot. You can leave your message after the beep."
        res_root.append(speak_elem)
        
        #adding the record elemnt in the xml response
        rec_elem = etree.Element('Record',action=action_url, maxLength="120", timeout="6")
        res_root.append(rec_elem)
        
        NoMsgElem = etree.Element('Speak')
        NoMsgElem.text = "Sorry. You didn't provide any message. Thank you and have a nice day!"
        res_root.append(NoMsgElem)
        
        return HttpResponse(etree.tostring(res_root), content_type="text/xml")