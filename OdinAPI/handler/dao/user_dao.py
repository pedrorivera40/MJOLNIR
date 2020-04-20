from .config.sqlconfig import db_config
from flask import jsonify
import psycopg2

# TODO: ALWAYS CHECK THE is_invalid field is false before every query. Otherise we are searching trhough records that technically do not exist


class UserDAO:
    def __init__(self):
        connection_url = "dbname={} user={} password={} host ={} ".format(
            db_config['database'],
            db_config['username'],
            db_config['password'],
            db_config['host']
        )
        self.default_permissions = [
            {
                "is_invalid": False,
                "permission_id": 13
            },
            {
                "is_invalid": False,
                "permission_id": 14
            },
            {
                "is_invalid": False,
                "permission_id": 15
            },
            {
                "is_invalid": False,
                "permission_id": 16
            },
            {
                "is_invalid": False,
                "permission_id": 17
            },
            {
                "is_invalid": False,
                "permission_id": 18
            },
            {
                "is_invalid": False,
                "permission_id": 19
            },
            {
                "is_invalid": False,
                "permission_id": 20
            },
            {
                "is_invalid": False,
                "permission_id": 21
            },
            {
                "is_invalid": False,
                "permission_id": 22
            },
            {
                "is_invalid": False,
                "permission_id": 23
            },
            {
                "is_invalid": False,
                "permission_id": 24
            },
            {
                "is_invalid": False,
                "permission_id": 25
            },
            {
                "is_invalid": False,
                "permission_id": 26
            },
            {
                "is_invalid": False,
                "permission_id": 27
            }]

        self.conn = psycopg2.connect(connection_url)

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
                    Select case when (select count(*) from dashboard_user where email =%s ) > 0
                    then 'yes' else 'no' end as emailTest,
                    case when (select count(*) from dashboard_user where username =%s AND is_invalid = FALSE ) >0
                    then 'yes' else 'no' end as usernameTest;
                    """
        cursor.execute(probeQuery, (email, username,))
        conflicts = cursor.fetchone()
        if(conflicts[0] == 'yes'):
            return 'UserError1'  # User with that email already exists in the system
        elif(conflicts[1] == 'yes'):
            return 'UserError2'  # User with that username already exists in the system
        else:
            # is_active and is_invalid are false by default because we want inactive, valid accounts upon creation.
            query = """
                    insert into dashboard_user(username, full_name, email,password_hash, is_active, is_invalid)
                    values (%s,%s, %s,%s, FALSE, FALSE) 
                    returning id, username, full_name, email, is_active, is_invalid;
                    """
            cursor.execute(query, (username, fullName, email, password,))
            newUser = cursor.fetchone()
            newUserID = newUser[0]
            # Call addUserPermision to create a new user with all permissions false by default.
            self.addUserPermissions(
                newUserID, self.default_permissions)
            if not newUser:
                return 'UserError3'
            self.commitChanges()
            return newUser

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
        query = 'select id, username, full_name, email, is_active, is_invalid from dashboard_user where is_invalid = FALSE;'
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
        # TODO check if user with that ID exits

        cursor = self.conn.cursor()
        query = """select id, username, full_name, email, is_active, is_invalid from dashboard_user
                    where id = %s
                    AND is_invalid = FALSE;
                """
        cursor.execute(query, (duid,))
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
        # TODO check if user with that Username exits

        query = """select id, username, full_name, email, is_active, is_invalid from dashboard_user
                    where username = %s
                    AND is_invalid = FALSE;
                """
        cursor.execute(query, (username,))
        user = cursor.fetchone()

        return user

    def getHashByUsername(self, username):
        """
        Gets a Dashboard user's hash given their username.

        This function accepts a username to perform a query to the database that
        gets a dashboard user's hash that matches the given username.

        Args:
            username: The username of the dashboboard user that needs to be fetched.

        Returns:
            A list containing the response to the database query
            containing the matching record for the given username.
        """
        cursor = self.conn.cursor()
        # TODO check if user with that Username exits

        query = """select password_hash from dashboard_user
                    where username = %s
                    AND is_invalid = FALSE;
                """
        cursor.execute(query, (username,))
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
        # TODO check if user with that Email exits

        query = """select id, username, full_name, email, is_active, is_invalid from dashboard_user
                    where email = %s
                    AND is_invalid = FALSE;
                """
        cursor.execute(query, (email,))
        users = cursor.fetchone()
        return users

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
        cursor = self.conn.cursor()
        # TODO Check that user with that ID exists
        query = """
                update dashboard_user
                set password_hash = %s
                where id = %s
                AND is_invalid = FALSE
                returning id, username, full_name, email, is_active, is_invalid;
                """
        cursor.execute(query, (password, duid,))
        users = cursor.fetchone()
        self.commitChanges()
        return users

    def updateDashUserPasswordByUsername(self, username, password):
        """
        Updates the password for the dashboard user with the given username and sets is_active status.

        This function accepts a username and a password hash and uses them 
        to update password in the record of the user with the matching ID.

        Args:
            username: The username of the user whose password must be updated.
            password: Temporary password provided by the sistem admin.
            new_password: New password set by the user.

        Returns:
            A list containing the response to the database query
            containing the matching record for the modified dashboard user.
        """
        cursor = self.conn.cursor()
        # TODO Check that user with that ID exists
        query = """
                update dashboard_user
                set password_hash = %s
                where username = %s
                AND is_invalid = FALSE
                returning id, username, full_name, email, is_active, is_invalid;
                """
        cursor.execute(query, (password, username,))
        users = cursor.fetchone()
        self.commitChanges()
        return users

    def updateDashUserInfo(self, duid, username, full_name, email, is_active):
        """
        Updates the username for the dashboard user with the given ID.

        This function accepts an ID and a username and uses them 
        to update username in the record of the user with the matching ID.

        Args:
            duid: The ID of the user whose username must be updated.
            username: The new username for the dashboard user.
            full_name: The new name for the dashboboard user.
            email: The new email for the dashboboard user.
            is_active: The new active status for the dashboard user.
        Returns:
            A list containing the response to the database query
            containing the matching record for the modified dashboard user.
        """
        cursor = self.conn.cursor()
        probeQuery = """
                    Select case when (select count(*) from dashboard_user where id != %s AND email =%s AND is_invalid = FALSE) > 0
                    then 'yes' else 'no' end as emailTest,
                    case when (select count(*) from dashboard_user where id != %s AND username =%s AND is_invalid = FALSE) > 0
                    then 'yes' else 'no' end as usernameTest;
                    """
        cursor.execute(probeQuery, (duid,email,duid,username,))
        conflicts = cursor.fetchone()
        if(conflicts[0] == 'yes'):
            return 'UserError1'  # User with that email already exists in the system.
        if(conflicts[1] == 'yes'):
            return 'UserError2'  # User with that username already exists in the system.

        query = """
                update dashboard_user
                set username = %s,
                full_name= %s,
                email=%s,
                is_active=%s
                where id = %s
                AND is_invalid = FALSE
                returning id, username, full_name, email, is_active, is_invalid;
                """
        cursor.execute(query, (username, full_name, email, is_active, duid,))
        users = cursor.fetchone()
        self.commitChanges()
        return users

    def toggleDashUserActive(self, duid):
        """
        Toogles a user's active status in the database.

        This function accepts an ID and uses it to togle the "is_active" field
        within the database depending on the current value.

        Args:
            duid: The ID of the user that will be toggled.

        Returns:
            A list with the response to the database query
            containing the matching record for the modified dashboard user.
        """
        cursor = self.conn.cursor()

        query = """
                update dashboard_user 
                set is_active= not is_active 
                WHERE id = %s
                AND is_invalid = FALSE
                returning id, username, full_name, email, is_active, is_invalid;
                """
        cursor.execute(query, (duid,))
        users = cursor.fetchone()
        self.commitChanges()
        return users

    def deactivateDashUserAccount(self, duid):
        """
        Sets a user's active status to false in the database.

        This function accepts an ID and uses it set the "is_active" field
        within the database to false.

        Args:
            duid: The ID of the user that will be deactivated.

        Returns:
            A list with the response to the database query
            containing the matching record for the modified dashboard user.
        """
        cursor = self.conn.cursor()

        query = """
                update dashboard_user 
                set is_active= False 
                WHERE id = %s
                AND is_invalid = FALSE
                returning id, username, full_name, email, is_active, is_invalid;
                """
        cursor.execute(query, (duid,))
        users = cursor.fetchone()
        self.commitChanges()
        return users

    def activateDashUserAccount(self, duid):
        """
        Sets a user's active status to true in the database.

        This function accepts an ID and uses it set the "is_active" field
        within the database to true.

        Args:
            duid: The ID of the user that will be activated.

        Returns:
            A list with the response to the database query
            containing the matching record for the modified dashboard user.
        """
        cursor = self.conn.cursor()

        query = """
                update dashboard_user 
                set is_active= TRUE 
                WHERE id = %s
                AND is_invalid = FALSE
                returning id, username, full_name, email, is_active, is_invalid;
                """
        cursor.execute(query, (duid,))
        users = cursor.fetchone()
        self.commitChanges()
        return users

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
        cursor = self.conn.cursor()
        query = """
                update dashboard_user 
                set is_invalid= TRUE,
                is_active = FALSE
                WHERE id = %s
                AND is_invalid = FALSE
                returning id, username, full_name, email, is_active, is_invalid;
                """
        cursor.execute(query, (duid,))
        users = cursor.fetchone()
        self.commitChanges()
        return users

    # This will not be used directly, it will be called on user add
    def addUserPermissions(self, duid, permissionsList):
        """
        Adds permissions to a newly created user.

        This fucntion will go thorugh the permissions list and apply them to 
        the user with the specified duid.

        Args:
            duid: The id of the user's whose permissions will be modified.
            pidList: A list of the permissions to add to the user.

        Returns:
            A list containing the response to the database query containing 
            the matching record of modiffied user permissions.
        """
        queryResults = []
        cursor = self.conn.cursor()

        # TODO finde better way to do this.
        # This makes sure it is a valid user.
        if self.getDashUserByID(duid) == None:
            return 'UserError4'
        if permissionsList == None:
            return 'UserError5'
        for permission in permissionsList:
            query = """
                    insert into user_permission (user_id, permission_id, is_invalid)
                    values (%s,%s, %s)
                    returning id, user_id, permission_id, is_invalid
            """
            cursor.execute(
                query, (duid, permission['permission_id'], permission['is_invalid'],))
            queryResults.append(cursor.fetchone())
        self.commitChanges()
        return queryResults

    # This will not be used directly, it
    def setUserPermissions(self, duid, permissionsList):
        """
        Sets permissions to a user.

        This fucntion will go thorugh the permissions list and set them depending on their value for
        the user with the specified duid.

        Args:
            duid: The id of the user's whose permissions will be modified.
            pidList: A list of the permissions to be set for the user.

        Returns:
            A list containing the response to the database query containing 
            the matching record of modified user permissions.
        """
        queryResults = []
        cursor = self.conn.cursor()
        # TODO find better way to do this.
        if self.getDashUserByID(duid) == None:
            return 'UserError4'
        if permissionsList == None:
            return 'UserError5'
        for permission in permissionsList:
            query = """
                    update user_permission 
                    set is_invalid = %s
                    where user_id= %s
                    AND permission_id = %s
                    returning permission_id, is_invalid
                    """
            cursor.execute(
                query, (permission['is_invalid'], duid, permission['permission_id'],))
            queryResults.append(cursor.fetchone())
        self.commitChanges()
        return queryResults

    def getUserPermissions(self, duid):
        """
        Get permissions for a user.

        Make a query to get the permissions of a user with the given permission ID,
        and return the records ordered by permission_id in ascendding fashion.

        Args:
            duid: Id of the user whose permissions are to be fetched.

        Returns:
            A ascending list ordered by permission_id containing the information
            about the user's permissions.
        """
        cursor = self.conn.cursor()
        # TODO find better way to do this.
        if self.getDashUserByID(duid) == None:
            return 'UserError4'
        query = """
                select permission_id, is_invalid 
                from user_permission 
                where user_id = %s
                Order by permission_id;
                """
        cursor.execute(query, (duid, ))
        queryResults = cursor.fetchall()
        self.commitChanges()
        return queryResults

    def getLoginAttempts(self, duid):
        """
        Returns the login attempts for a user.

        Performs a query to the database that returns the current number 
        of login attempts for the user with the given username.

        Args:
            username: Username of user for which to fetch login attempts.

        Returns:
            Current number of login attempts.
        """
        cursor = self.conn.cursor()
        query = """
                select login_attempts 
                from dashboard_user
                where id = %s
                and is_invalid=False;
                """
        cursor.execute(query, (duid, ))
        attempts = cursor.fetchone()
        return attempts

    def setLoginAttempts(self, duid, attempts):
        """
        Sets the value of login attempts for a user.

        Performs a query to the database that sets the current number 
        of login attempts for the user with the given username.

        Args:
            username: Username of user for which to set login attempts.

        Returns:
            Current number of login attempts.
        """
        cursor = self.conn.cursor()
        query = """
                update dashboard_user 
                set login_attempts=%s
                where id=%s
                and is_invalid=False
                returning login_attempts;
                """
        cursor.execute(query, (attempts, duid, ))
        attempts = cursor.fetchone()
        self.commitChanges()
        return attempts

    def commitChanges(self):
        self.conn.commit()
