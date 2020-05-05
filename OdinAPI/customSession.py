class CustomSession(object):

    def __init__(self, key):
        self.theSession = {}

    def setVal(self, key, value):
        if value == None or value == '':
            return
        self.theSession[key] = value

    def getVal(self, key):
        return self.theSession.get(key,'Invalid Session')
