import random, uuid, os, datetime, re, time

class Helper:
    
    def getFilePath(instance,filename):
        now = datetime.datetime.now()
        month = str(now.month)
        day = str(now.day)
        rand_name = uuid.uuid4().hex;
        new_name = str(rand_name)+'.'+str(filename)
        path = os.path.join("file/"+month+"/"+day+"/", new_name)
        return path
    
    def getHostString(self,req):
        protocol = req.META.get("SERVER_PORT",False)
        if protocol == "443":
            hoststring = "https://"
        else:
            hoststring = "http://"
        host = req.META.get("HTTP_HOST", req.META.get("SERVER_NAME",False))
        if host is False:
            host = "sendboro.com"
        hoststring += host
        return hoststring 
    
    def getFormattedType(self,type, name, ext_req=False):

        pattern = re.compile("\.([^\.]{2,6}$)")
        res = pattern.search(name)
        if res:
            if ext_req:
                return res.group(1)
            else:
                file_category = self.processExt(res.group(1))
                if file_category:
                    return file_category
            
        if len(type) == 0:
            return type
        pattern = re.compile("^([^\/]+)\/")
        res = pattern.search(type)
        return res.group(1)
    
    def processExt(self,extension):
        ext_array = [('document',
                        ['ppt','csv','doc','docx','ppt','pptx','pdf','odp','odt','pps','xls','xlsx']
                      ),
                     ('zip',
                        ['zip','gz','7z','gz2','xz','bz2','xz2','rar']
                      ),
                     ('source',
                        ['php','js','py','aspx','jsp'])
                     ]
        
        for extgroup in ext_array:
            for ext in extgroup[1]:
                if ext == extension:
                    return extgroup[0]
                
        return None
    
class Time:
    
    def __init__(self,timefromdb):
        stripped_t = timefromdb[:-6]
        self.t = t = time.strptime(stripped_t, '%Y-%m-%d %H:%M:%S.%f')
        self.diff = round((datetime.datetime.utcnow() - datetime.datetime(t.tm_year,t.tm_mon,
                                                           t.tm_mday,t.tm_hour,
                                                           t.tm_min,t.tm_sec)).total_seconds())
    
    def getDiff(self):
        
        if self.diff/60 < 1:
            return str(self.diff)+' seconds ago'
        
        elif self.diff/3600 < 1:
            minute = round(self.diff/60)
            if minute == 1:
                plural = ''
            else:
                plural = 's'
            return str(minute)+' minute'+plural+' ago'
        
        elif self.diff/(3600*24) < 1:
            hour = round(self.diff/3600)
            if hour == 1:
                plural = ''
            else:
                plural = 's'
            return str(hour)+' hour'+plural+' ago'
        
        elif self.diff/86400 > 1:
            day = round(self.diff/86400)
            if day == 1:
                plural = ''
            else:
                plural = 's'
            return str(day)+' day'+plural+' ago'                                    
        
    def getTooltip(self):
        
        month = ['Jan','Feb','Mar','Apr', 'May','Jun','Jul','Aug', 'Sep','Oct','Nov','Dec']
        
        current = datetime.datetime.now()
        
        curr_year = current.strftime('%Y')
        curr_month = current.strftime('%m')
        curr_day = current.strftime('%d')
        
        if self.t.tm_year == int(curr_year):
            
            if self.t.tm_mon == int(curr_month) \
            and self.t.tm_mday == int(curr_day):
                date = 'Today'
            elif self.t.tm_mon == int(curr_month) \
            and int(curr_day) - int(self.t.tm_mday) == 1:
                date = 'Yesterday'
            else:
                date = ('0'+str(self.t.tm_mday))[-2:]+' '+str(month[self.t.tm_mon-1])
                
        else:
            date = ('0'+str(self.t.tm_mday))[-2:]+' '+str(month[self.t.tm_mon-1])+', '+str(self.t.tm_year)
            
        return str(date)+' '+('0'+str(self.t.tm_hour))[-2:]+':'+('0'+str(self.t.tm_min))[-2:]  

class Random():
    # type: 1 for numeric; 2 for alphabets; 3 for alphanumeric; 4 for alphanumeric+extra
    type = 1
    nonce = None
    min_num_char = None
    max_num_char = None
    
    def __init__(self,type,min,max):
        self.type = type
        self.min_num_char = min
        self.max_num_char = max
    
    def create(self):
        if self.type==1:
            self.create_numeric()
        return self.nonce
        
    
    def create_numeric(self):
        range_bottom = 10 ** (self.min_num_char-1)
        range_top = (10 ** self.max_num_char) - 1
        self.nonce = random.randrange(range_bottom,range_top)
        
class UserTrace():
    ipaddress = None
    uastring = None
    request = None
    
    def __init__(self,req):
        self.request = req
        
    def getIp(self):
        x_forwarded = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            ipaddress = x_forwarded.split(',')[-1].strip()
        else:
            ipaddress = self.request.META.get('REMOTE_ADDR')
        return ipaddress
    
    def getUastring(self):
        return self.request.META.get('HTTP_USER_AGENT')
    