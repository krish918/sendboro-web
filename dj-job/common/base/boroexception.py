#custom exception class

class BoroException(Exception):
    
    def __init__(self, message, errorcode):
        
        #calling base class constructor
        super(BoroException, self).__init__(message,errorcode)
        
        self.code = errorcode
        self.message = message
        