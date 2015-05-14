import plivo

class TextMessage():
    
    auth_id = "MAYTM5YZM0MMVMNGNHZD"
    auth_token = "NjEzZTFmNDUxMzlkZGRhNGEzNjM0NGQzYTM2NDE0"
    
    def __init__(self,text,dest,src='SNDBOR'):
        self.destination = dest
        self.text = text
        self.source = src
        
    def send(self):
        p = plivo.RestAPI(self.auth_id, self.auth_token)
        params = {
                  'src' : self.source,
                  'dst' : self.destination,
                  'text': self.text,
                  } 
        try:
            response = p.send_message(params)
        except TypeError:
            pass
        except:
            raise