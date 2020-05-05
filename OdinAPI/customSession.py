class CustomSession(object):

    def __init__(self):
        self.sessionList = []

    def setLoggedUser(self, value):
        theSession = {}
        if value == None or value == '':
            return
        theSession["username"] = value
        self.sessionList.append(theSession)

    def isLoggedIn(self, username):
        try:
            loggedUser = next(session for session in self.sessionList if session.get("username", "Invalid Session") == username)
            return loggedUser
        except:
            return None
