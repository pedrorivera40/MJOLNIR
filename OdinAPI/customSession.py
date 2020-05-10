class CustomSession(object):

    def __init__(self):
        self.sessionList = []

    def setLoggedUser(self, value):
        """
        Add logged in user, to the custon session list.

        Take in the username for the user that just logged in and added to the custom session list.

        Args: 
            value: The username of the reciently logged in user to be added to the session list.
        """
        theSession = {}
        if value == None or value == '':
            return
        theSession["username"] = value
        self.sessionList.append(theSession)

    def isLoggedIn(self, username):
        """
        Function to check if the user with the given uisername is logged in.

        This fucntion takes in the username to be queried in order to determined wether that user
        has a valid active session or not.

        Args:
            username: The username of the user whose session status must be determined

        Returns:
            Returns a dictionary containing the logged in user is the user has an active session and None
            if there is no active session.
        """
        loggedUser = next((session for session in self.sessionList if session.get("username", "Invalid Session") == username), None)
        return loggedUser

    def logout(self, username):
        """
        Deletes the session for the user with the provided username.

        Deletes the user with the provided username from the active session list.
        """
        self.sessionList = [session for session in self.sessionList if not (session['username'] == username)]
        loggedUser = next((session for session in self.sessionList if session.get("username", "Invalid Session") == username),None)
        return loggedUser == None