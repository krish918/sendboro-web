#custom class for collecting all constants used in app
class Const:
    
    #constants for error handling during authentication
    
    INVALID_PHONE = 2
    INVALID_DIALCODE = 3
    INVALID_USERNAME = 4
    USERNAME_NOTEXIST = 5
    AUTH_ERROR = -1
    
    #Constants for Borouser to diff Signup and Signin
    SIGNUP = 1
    SIGNIN = 2 
    
    #constants for polling server to challenge veri code
    VALID_CODE = 1
    INVALID_CODE = -2
    RESOLVED_CODE = -3
    EMPTY_POLL = 3
    POLL_ERROR = -1
    
    #error for User class Hierarchy
    INSTANCE_ERROR = -1
    
    GEN_ERROR = 99
    #error for voicecall API
    CALL_ERROR = 4;

    STATUS_OK = 'ok'
    STATUS_FAILED = 'failed'
    INVALID_USERNAME = 'invalid_username'
    ALREADY_EXIST = 'already_exist'
    STATUS = 'status'