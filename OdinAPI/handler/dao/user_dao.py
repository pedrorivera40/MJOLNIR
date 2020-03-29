from .config.sqlconfig import db_config
from flask import jsonify
import psycopg2


class UserDAO:
    def __init__(self):
        connection_url = "dbname={} user={} password={} host ={} ".format(
            db_config['database'],
            db_config['username'],
            db_config['password'],
            db_config['host']
        )
        self.conn = psycopg2.connect(connection_url)

    def getAllDashUsers(self):
        """
        Gets all dashboard users.

        This function performs a query to the database to get all
        dashboard users in the system.

        Returns:
            A list containing the response to the database query
            containing all the dashboard users in the system.
        """
        cursor = self.conn.cursor()
        query = 'select id, username, full_name, email, is_active, is_invalid from dashboard_user;'
        cursor.execute(query,)
        users = []
        for row in cursor:
            users.append(row)
        
        return users

    def getDashUserByID(self, duid):
        """
        Gets a single dashboard user given their ID.

        This function uses an ID to perform a query to the database that
        gets a dashboard user in the system that matches the given ID.

        Args:
            duid: The ID of the dashboboard user that needs to be fetched.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the given ID.
        """
        cursor = self.conn.cursor()
        query = """select id, username, full_name, email, is_active, is_invalid from dashboard_user
                    where id = %s;
                """
        cursor.execute(query,(duid,))
        user = cursor.fetchone()
        return user
        
    def getDashUserByUsername(self, username):
        """
        Gets a single Dashboard user given their username.

        This function accepts a username to perform a query to the database that
        gets a dashboard user in the system that matches the given username.

        Args:
            username: The username of the dashboboard user that needs to be fetched.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the given username.
        """
        cursor = self.conn.cursor()
        query = """select id, username, full_name, email, is_active, is_invalid from dashboard_user
                    where username = %s;
                """
        cursor.execute(query,(username,))
        user = cursor.fetchone()
        
        return user

    def getDashUserByEmail(self, email):
        """
        Gets a single Dashboard user given their email.

        This function accepts an email to perform a query to the database that
        gets a dashboard user in the system that matches the given email.

        Args:
            email: The email of the dashboboard user that needs to be fetched.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the given email.
        """
        cursor = self.conn.cursor()
        query = """select id, username, full_name, email, is_active, is_invalid from dashboard_user
                    where email = %s;
                """
        cursor.execute(query,(email,))
        users = cursor.fetchone()
        return users

    def addDashUser(self, username, fullName, email, password):
        """
        Adds a new Dashboard user with the provided information.

        This function accepts a first name, last name, email and password, 
        to perform a query to the database that adds a new dashboard user 
        to the system with the provided information.

        Args:
            firstName: The first name of the new dashboboard user.
            lastName: The last name of the new dashboboard user.
            email: The email of the new dashboboard user.
            password: The hash of the password for the new dashboboard user.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the new dashboard user.
        """ 
        
        cursor = self.conn.cursor()
        # Make sure the user being added does not exist already:
        probeQuery = """
                    Select case when (select count(*) from dashboard_user where email =%s) > 0
                    then 'yes' else 'no' end as emailTest,
                    case when (select count(*) from dashboard_user where username =%s) >0
                    then 'yes' else 'no' end as usernameTest;
                    """
        cursor.execute(probeQuery, (email, username,))
        conflicts = cursor.fetchone()
        if(conflicts[0]=='yes'):
            return 'UserError1'
        elif(conflicts[1]=='yes'):
            return 'UserError2'
        else:
            # is_active and is_invalid are false by default because we want inactive, valid accounts upon creation.
            query = """
                    insert into dashboard_user(username, full_name, email,password_hash, is_active, is_invalid)
                    values (%s,%s, %s,%s, FALSE, FALSE) 
                    returning id, username, email;
                    """
            cursor.execute(query,(username,fullName, email, password,))
            newUser = cursor.fetchone()
            if not newUser:
                return 'UserError3'
            self.commitChanges()
            return newUser

    def updateDashUserPassword(self, duid, password):
        """
        Updates the password for the dashboard user with the given ID.

        This function accepts an ID and a password hash and uses them 
        to update password in the record of the user with the matching ID.

        Args:
            duid: The ID of the user whose password must be updated.
            password: The hash of the new password for the dashboboard user.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified dashboard user.
        """
        return None

    def updateDashUserUsername(self, duid,username):
        """
        Updates the username for the dashboard user with the given ID.

        This function accepts an ID and a username and uses them 
        to update username in the record of the user with the matching ID.

        Args:
            duid: The ID of the user whose username must be updated.
            username: The new username for the dashboard user.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified dashboard user.
        """
        return None

    def markDashUserInactive(self, duid):
        """
        Marks a user as inactive in the database.

        This function accepts an ID and uses it to set the "active" field
        within the database as inactive.

        Args:
            duid: The ID of the user that will be deactivated.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified dashboard user.
        """
        return None

    def markDashUserActive(self, duid):
        """
        Marks a user as active in the database.

        This function accepts an ID and uses it to set the "active" field
        within the database as active.

        Args:
            duid: The ID of the user that will be activated.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified dashboard user.
        """
        return None

    def removeDashUser(self, duid):
        """
        Invalidates a user in the database.

        This function accepts an ID and uses it to set the valid field
        within the database as invalid, this acts as a deletion of the user
        from the system.

        Args:
            duid: The ID of the user that will be invalidated.
            
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified dashboard user.
        """
        return None

    def commitChanges(self):
        self.conn.commit()
