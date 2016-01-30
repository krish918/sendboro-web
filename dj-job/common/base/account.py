# for performing account related activities

class Account:
        
    def __init__(self, userObj):
        if isinstance(userObj, Borouser):
            self.user = userObj
        else:
            raise Exception("Invalid User Object")
        
    def signup(self):
        response = self.user.addraw()
        response['success'] = True
        return response
    
    def signin(self, loginName):
        response = self.user.attemptlogin()
        if loginName is not None:
            response['uname'] = loginName
        response['success'] = True 
        return response