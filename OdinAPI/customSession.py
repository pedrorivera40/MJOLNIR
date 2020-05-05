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
        loggedUser = next(session for session in self.sessionList if session["username"] == username)
        return loggedUser
