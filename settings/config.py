
class Common(object):
    XYZ_API_KEY = 'AJSKDF234328942FJKDJ32'
    XYZ_API_SECRET = 'KDJFKJ234df234fFW3424@#ewrFEWF'

class Local(Common):
    DB_URI = 'local/db/uri'
    DEBUG = True

class Production(Common):
    DB_URI = 'remote/db/uri'
    DEBUG = False

class Staging(Production):
    DEBUG = True
