from handler.dao.config.sqlconfig import db_config
import psycopg2

class CustomSession(object):

    def __init__(self):
        self.connection_url = None
        self.conn = None
        self.cursor = None

    def initConnection(self):
        self.connection_url = "dbname={} user={} password={} host ={} ".format(
            db_config['database'],
            db_config['username'],
            db_config['password'],
            db_config['host']
        )
        self.conn = psycopg2.connect(self.connection_url)
        self.cursor = self.conn.cursor()

    def setLoggedUser(self, username):
        """
        Add logged in user, to the custon session list.

        Take in the username for the user that just logged in and added to the custom session list.

        Args: 
            username: The username of the reciently logged in user to be added to the session list.
        """
        self.initConnection()
        if(self.checkLoggedIn(username)):
            return
        try:
            self.cursor.execute("INSERT INTO session VALUES (%s)",(username,))
            self.conn.commit()
        except Exception as e:
            print(e)
        self.conn.close()

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
        self.cursor.execute('SELECT * FROM session WHERE username= %s ', (username,))
        loggedUser = self.cursor.fetchone()
        self.conn.close()
        if(bool(loggedUser)):
            return loggedUser[0]
        return None

    def checkLoggedIn(self, username):
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
        self.cursor.execute('SELECT * FROM session WHERE username= %s ', (username,))
        loggedUser = self.cursor.fetchone()
        if(bool(loggedUser)):
            
            return loggedUser[0]
        return None

    def logout(self, username):
        """
        Deletes the session for the user with the provided username.

        Deletes the user with the provided username from the active session list.
        """
        self.initConnection()
        try:
            self.cursor.execute('DELETE FROM session WHERE username= %s ', (username,))
            self.conn.commit()

        except:
            print('No session in stored.')
        self.conn.close()
