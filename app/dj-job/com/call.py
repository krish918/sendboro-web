import plivo, urllib
from com.credential import auth_id, auth_token, auth_phone

class VoiceCall():
    def __init__(self, phone, answer_url):
        self.phone = phone
        self.answer_url = answer_url
    
    def call(self):
        params = {
                  'to': self.phone,
                  'from': auth_phone,
                  'answer_url': self.answer_url,
                  'answer_method': "POST",
                  }
        
        try:
            p = plivo.RestAPI(auth_id, auth_token)
            return p.make_call(params)
        except:
            raise