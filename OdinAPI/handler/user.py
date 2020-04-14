from flask import jsonify, session
from auth import createHash, verifyHash, generateToken, rulesMatch
from .dao.user_dao import UserDAO


class UserHandler:
    def mapUserToDict(self, record):
        """
        Converts a record returned by the DAO into a dictionary.
        """
        userDictionary = {}
        userDictionary['id'] = record[0]
        userDictionary['username'] = record[1]
        userDictionary['full_name'] = record[2]
        userDictionary['email'] = record[3]
        userDictionary['is_active'] = record[4]
        userDictionary['is_invalid'] = record[5]

        return userDictionary

    def mapPermissionsToDict(self, record):
        """
        Converts results returned by DAO into a dictionary.
        """
        permissionsDictionary = {}
        permissionsDictionary['permission_id'] = record[0]
        permissionsDictionary['is_invalid'] = record[1]
        return permissionsDictionary

    def mapHash(self, record):
        """
        Converts results returned by DAO into a dictionary.
        """
        permissionsDictionary = {}
        permissionsDictionary['hash'] = record[0]
        return permissionsDictionary

    def addDashUser(self, username, fullName,email, password):
        """
        Adds a new Dashboard user with the provided information.

        Calls the UserDAO to add a new dashboard user and maps the result to
        to a JSON that contains the desired record. That JSON object 
        is then returned.

        Args:
            username: The usernamename of the new dashboboard user.
            full_name: The name of the new dashboboard user.
            email: The email of the new dashboboard user.
            password: The hash of the password for the new dashboboard user.
            
        Returns:
            A JSON containing all the user with the new dashboard user.
        """
        # Verify password complies with the rules
        if not rulesMatch(password):
            return jsonify(Error="""Password should contain At least 1 upercase letter,
            1 lowecase letter, at least 1 number, at least 1 symbol, and is between 
            10 and 64 characters long."""), 400

        # Hash the password 
        hashedPassword = createHash(password)

        dao = UserDAO()
        res = dao.addDashUser(username, fullName,email, hashedPassword)

        if res == 'UserError1':
            return jsonify(Error='Email has been registered.'),400 # Conflict with the current state of the server
        elif res == 'UserError2':
            return jsonify(Error='Username is already taken.'),400
        elif res == 'UserError3':
            return jsonify(Error="New user not created"), 400
        else:
            mappedUser = self.mapUserToDict(res)
            dao.setLoginAttempts(mappedUser['id'],0) #sets login attempts to 0 upon creation.
            return jsonify(User=mappedUser),201

    def getAllDashUsers(self):
        """
        Gets all dashboard users.

        Calls the UserDAO to get all users and maps the result to
        to a JSON that contains all the users in the system. That
        JSON object is then returned.

        Returns:
            A JSON containing all the dashboard users in the system. 
        """
        dao = UserDAO()
        userList = dao.getAllDashUsers()

        if userList == None:
            return jsonify(Error='No users found in the system'), 404
        
        mappedUsers = []
        for user in userList:
            mappedUsers.append(self.mapUserToDict(user)) 
        
        return jsonify(Users=mappedUsers),200 #200 == OK
        
    def getDashUserByID(self, duid):
        """
        Gets a single dashboard user given their ID.

        Calls the UserDAO to get a user by ID and maps the result to
        to a JSON that contains the desired record. That JSON object 
        is then returned.

        Args:
            duid: The ID of the dashboboard user that needs to be fetched.
            
        Returns:
            A JSON containing all the user with the given ID.
        """
        dao = UserDAO()
        fetchedUser = dao.getDashUserByID(duid)
        if fetchedUser == None:
            return jsonify(Error="No user found in the system with that id."), 404
        
        mappedUser = self.mapUserToDict(fetchedUser)
        return jsonify(User=mappedUser),200 #200 == OK
        
    def getDashUserByUsername(self, username):
        """
        Gets a single Dashboard user given their username.

        Calls the UserDAO to get a user by username and maps the result to
        to a JSON that contains the desired record. That JSON object 
        is then returned.

        Args:
            username: The username of the dashboboard user that needs to be fetched.
            
        Returns:
            A JSON containing all the user with the given username.
        """
        dao = UserDAO()
        fetchedUser = dao.getDashUserByUsername(username)
        if fetchedUser == None:
            return jsonify(Error="No user found in the system with that username."), 404
        
        mappedUser = self.mapUserToDict(fetchedUser)
        return jsonify(User=mappedUser),200 #200 == OK

    def getDashUserByEmail(self, email):
        """
        Gets a single Dashboard user given their email.

        Calls the UserDAO to get a user by username and maps the result to
        to a JSON that contains the desired record. That JSON object 
        is then returned.

        Args:
            email: The email of the dashboboard user that needs to be fetched.
            
        Returns:
            A JSON containing all the user with the given email.
        """
        dao = UserDAO()
        fetchedUser = dao.getDashUserByEmail(email)
        if fetchedUser == None:
            return jsonify(Error="No user found in the system with that email."), 404
        
        mappedUser = self.mapUserToDict(fetchedUser)
        return jsonify(User=mappedUser),200 #200 == OK

    def login(self, username, password):
        """
        Gets a dashboard's user password hash given their username.

        Calls the UserDAO to get a user's password hash given their username 
        and maps the result to a JSON that contains the desired record. 
        That JSON object is then returned.

        Args:
            username: The username of the dashboboard user that needs to be fetched.
            password: The password of the dashboard user
        Returns:
            A JSON containing all the user's hash.
        """
        dao = UserDAO()

        #get user by username
        user = dao.getDashUserByUsername(username) 

        # verify is user exists
        if user == None:
            # Login attempts do not increase because username does not exist.
            return jsonify(Error="Username or Password are incorrect."), 400
        # get user id , whic is position 0 of the user tupple.
        duid = user[0] 
        attempts = dao.getLoginAttempts(duid)[0] #get current number of attempts
        
        if attempts == 3 or user[4] == False : # If there are 3 failed login attempts, deactivate account.
            dao.deactivateDashUserAccount(duid)
            return jsonify(Error='Account is locked.'), 401

        fetchedHash = dao.getHashByUsername(username)
        if fetchedHash == None: #TODO this may be repeated code.
            # Login attempts do not increase because username does not exist.
            return jsonify(Error="Username or Password are incorrect."), 400
        
        mappedHash = self.mapHash(fetchedHash)
        #TODO AES encryption.
        if verifyHash(password, mappedHash['hash']):
            # User provided correct password
            token = generateToken(username)
            loginInfo = {
                'user': username,
                'token': token
            }
            
            dao.setLoginAttempts(duid,0)
            session['username'] = loginInfo['user']
            return jsonify(auth=loginInfo), 201

        dao.setLoginAttempts(duid,attempts+1)
        return jsonify(Error="Username or Password are incorrect."), 400

    def updateDashUserPassword(self, duid, password):
        """
        Updates the password for the dashboard user with the given ID.

        Calls the UserDAO to update the password of a dashboard user. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            duid: The ID of the user whose password must be updated.
            password: The hash of the new password for the dashboboard user.
            
        Returns:
            A JSON containing all the user with the updated dashboard user.
        """
        # Verify password complies with the rules
        if not rulesMatch(password):
            return jsonify(Error="""Password should contain At least 1 upercase letter,
            1 lowecase letter, at least 1 number, at least 1 symbol, and is between 
            10 and 64 characters long."""), 400
        # Hash password 
        hashedPassword = createHash(password)
        dao = UserDAO()
        res = dao.updateDashUserPassword(duid, hashedPassword)
        if res == None:
            return jsonify(Error='No user found in the system with that id.'), 404
        
        ## When password is reset, login attempts are set to 0
        dao.activateDashUserAccount(duid) #Set account active to true.
        dao.setLoginAttempts(duid,0)
        return jsonify(User=self.mapUserToDict(res)),201

    def updateDashUserInfo(self, duid,username, full_name,email,is_active):
        """
        Updates the username for the dashboard user with the given ID.

        Calls the UserDAO to update the username of a dashboard user. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            duid: The ID of the user whose username must be updated.
            username: The new username for the dashboard user.
            full_name: The new name for the dashboboard user.
            email: The new email for the dashboboard user.
            is_active: The new active status for the dashboard user.
        Returns:
            A JSON containing all the user with the updated dashboard user. 
        """
        dao = UserDAO()
        res = dao.updateDashUserInfo(duid, username, full_name,email,is_active)
        if res == None:
            return jsonify(Error='No user found in the system with that id.'), 404
        if res == 'UserError1':
            return jsonify(Error='Email already taken.'), 400
        elif res == 'UserError2':
            return jsonify(Error='Username already taken.'), 400
        else:
            return jsonify(User=self.mapUserToDict(res)),201

    #TODO: Update documentation of the API merge mard inactive/active to toggle active
    def toggleDashUserActive(self, duid):
        """
        Toggle the active status of a dashboard user.

        Calls the UserDAO to toggle a dashboard user account's active state. 
        It then maps the result to a JSON that contains the desired record. 
        That JSON object is then returned.

        Args:
            duid: The ID of the user that will be toggled.
            
        Returns:
            A JSON containing the updated dashboard user.
        """
        dao = UserDAO()
        res = dao.toggleDashUserActive(duid)
        if res == None:
            return jsonify(Error='No user found in the system with that id.'), 404
        return jsonify(User=self.mapUserToDict(res)),201

    def removeDashUser(self, duid):
        """
        Invalidates a user in the database.

        Calls the UserDAO to invalidate a dashboard user's account. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            duid: The ID of the user that will be invalidated.
            
        Returns:
            A JSON containing all the user with the updated dashboard user.
        """
        dao = UserDAO()
        res = dao.removeDashUser(duid)
        if res == None:
            return jsonify(Error='No user found in the system with that id.'), 404
        return jsonify(User=self.mapUserToDict(res)),201

    def setUserPermissions(self,duid,permissionsList):
            """
            Adds permissions to a user.

            This fucntion will go thorugh the permissions list and apply them to 
            the user with the specified duid.

            Args:
                duid: The id of the user's whose permissions will be modified.
                permissionsList: A list of the permissions to add to the user.
            
            Returns:
                A list containing the response to the database query containing 
                the matching record of modiffied user permissions.
            """
            for permission in permissionsList: #If at least one of the parameters of one the indexes is None, scrap the request
                if 'permission_id' not in permission or 'is_invalid' not in permission:
                    return jsonify(Error='Bad Request'), 400

            dao = UserDAO()
            resultList = dao.setUserPermissions(duid, permissionsList)
            if resultList == 'UserError4':
                return jsonify(Error='No User found in the system with that id.'), 404
            if resultList == 'UserError5':
                return jsonify(Error='Permissions cant be empty.'), 400 # Bad request

            mappedPermissions = []
            for row in resultList:
                mappedPermissions.append(self.mapPermissionsToDict(row))
            return jsonify(Permissions=mappedPermissions),201

    def getUserPermissions(self,duid):
        """
        Get permissions for a user.

        Get the permissions of a user with the given permission ID.

        Args:
            duid: Id of the user whose permissions are to be fetched.

        Returns:
            A list of permission dictionnaries ordered by permission id in ascending fashion.
        """
        dao = UserDAO()
        permisionsList = dao.getUserPermissions(duid)
        if permisionsList == 'UserError4':
            return jsonify(Error='No User found in the system with that id.'), 404
        mappedPermissions = []
        for row in permisionsList:
            mappedPermissions.append(self.mapPermissionsToDict(row))
        return jsonify(Permissions=mappedPermissions),200