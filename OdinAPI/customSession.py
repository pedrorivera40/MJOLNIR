import sqlite3


class CustomSession(object):

    def __init__(self):
        self.connection = sqlite3.connect('userSessions.db')
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute('''CREATE TABLE IF NOT EXISTS sessions (user text UNIQUE) ''')
        except:
            print('table already exists')
        
        self.connection.commit()
        self.connection.close()

    def initConnection(self):
        self.connection = sqlite3.connect('userSessions.db')
        self.cursor = self.connection.cursor()

    def setLoggedUser(self, username):
        """
        Add logged in user, to the custon session list.

        Take in the username for the user that just logged in and added to the custom session list.

        Args: 
            username: The username of the reciently logged in user to be added to the session list.
        """
        self.initConnection()
        self.cursor.execute("INSERT OR IGNORE INTO sessions VALUES (?)",(username,))
        self.connection.commit()
        self.connection.close()

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
        self.initConnection()
        self.cursor.execute('SELECT * FROM sessions WHERE user= ? ', (username,))
        self.connection.commit()
        loggedUser = self.cursor.fetchone()
        self.connection.close()
        if(bool(loggedUser)):
            return loggedUser[0]
        return None

    def logout(self, username):
        """
        Deletes the session for the user with the provided username.

        Deletes the user with the provided username from the active session list.
        """
        self.initConnection()
        self.cursor.execute('DELETE FROM sessions WHERE user= ? ', (username,))
        self.connection.commit()
        loggedUser = self.cursor.fetchone()
        return loggedUser == None