import plivo
from com.credential import auth_id, auth_token

class TextMessage():
    
    def __init__(self,text,dest,src='SNDBOR'):
        self.destination = dest
        self.text = text
        self.source = src
        
    def send(self):
        p = plivo.RestAPI(auth_id, auth_token)
        params = {
                  'src' : self.source,
                  'dst' : self.destination,
                  'text': self.text,
                  } 
        try:
          response = p.send_message(params)
          #pass
        except TypeError:
            pass
        except:
            raise
