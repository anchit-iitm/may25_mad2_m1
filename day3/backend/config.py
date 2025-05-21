class Config():
    SECURITY_LOGIN_URL = '/SiGnIn'
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authorization'



class localDev(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SECRET_KEY = "Shhhhh.... its a secret"
    SECURITY_JOIN_USER_ROLES = True

    DEBUG = True

class production(Config):
    DEBUG = False