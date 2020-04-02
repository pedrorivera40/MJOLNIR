from flask import jsonify
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
        permissionsDictionary['id'] = record[0]
        permissionsDictionary['user_id'] = record[1]
        permissionsDictionary['permission_id'] = record[2]
        permissionsDictionary['is_invalid'] = record[3]
        return permissionsDictionary

    def addDashUser(self, username, fullName,email, password):
        """
        Adds a new Dashboard user with the provided information.

        Calls the UserDAO to add a new dashboard user and maps the result to
        to a JSON that contains the desired record. That JSON object 
        is then returned.

        Args:
            firstName: The first name of the new dashboboard user.
            lastName: The last name of the new dashboboard user.
            email: The email of the new dashboboard user.
            password: The hash of the password for the new dashboboard user.
            
        Returns:
            A JSON containing all the user with the new dashboard user.
        """
        dao = UserDAO()
        res = dao.addDashUser(username, fullName,email, password)
        if res == 'UserError1':
            return jsonify(Error='Email has been registered.')
        elif res == 'UserError2':
            return jsonify(Error='Username is already taken.')
        elif res == 'UserError3':
            return jsonify(Error="New user not created")
        else:
            return jsonify(User=self.mapUserToDict(res)),201

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
            return jsonify(Error="No users found in the system."), 404
        
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
        dao = UserDAO()
        res = dao.updateDashUserPassword(duid, password)
        if res == None:
            return jsonify(Error='No user found in the system with that id.'), 404
        return jsonify(User=self.mapUserToDict(res)),201

    def updateDashUserUsername(self, duid,username):
        """
        Updates the username for the dashboard user with the given ID.

        Calls the UserDAO to update the username of a dashboard user. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            duid: The ID of the user whose username must be updated.
            username: The new username for the dashboard user.
            
        Returns:
            A JSON containing all the user with the updated dashboard user. 
        """
        dao = UserDAO()
        res = dao.updateDashUserUsername(duid, username)
        if res == None:
            return jsonify(Error='No user found in the system with that id.'), 404
        if res == 'UserError2':
            return jsonify(Error='Username already taken.')
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

    def addUserPermissions(self,duid,pidList):
            """
            Adds permissions to a user.

            This fucntion will go thorugh the permissions list and apply them to 
            the user with the specified duid.

            Args:
                duid: The id of the user's whose permissions will be modified.
                pidList: A list of the permissions to add to the user.
            
            Returns:
                A list containing the response to the database query containing 
                the matching record of modiffied user permissions.
            """
            dao = UserDAO()
            permisionsList = dao.addUserPermissions(duid, pidList)
            if permisionsList == 'UserError4':
                return jsonify(Error='No User found in the system with that id.'), 404
            if permisionsList == 'UserError5':
                return jsonify(Error='Permissions cant be empty.'), 400 # Bad request
            mappedPermissions = []
            for row in permisionsList:
                mappedPermissions.append(self.mapPermissionsToDict(row))
            return jsonify(Permissions=mappedPermissions),201