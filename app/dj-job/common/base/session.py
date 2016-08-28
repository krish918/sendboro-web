from common.models import Session
from common.utils.general import UserTrace

class Session():
    def __init__(self,request, user):
        self.req = request
        self.user = user
        
    def Create(self):
        #getting ip and uastring
        trace = UserTrace(self.req)
        ip = trace.getIp()
        ua = trace.getUastring()
                                
        #inserting in session relation
        sess = self.user.session_set.create(uastring=ua, ipaddress=ip)
        hashid = self.req.session['hashid']
        # claro viejo session
        self.req.session.clear()
        
        #setting session objects
        self.req.session['user_id'] = self.user.userid
        self.req.session['session_id'] = sess.sessionid
        self.req.session['promise'] = hashid