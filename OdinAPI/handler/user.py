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
    def mapNewUserToDict(self, record):
        """
        Converts a record returned by the DAO into a dictionary.
        """
        
        userDictionary = {}
        userDictionary['id'] = record[0]
        userDictionary['username'] = record[1]
        userDictionary['email'] = record[2]

        return userDictionary

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
        
        #TODO: Tell everyone that 201 is cor creates.
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
        #TODO: Tell everyone that 201 is cor creates.
        return jsonify(Users=mappedUser),200 #200 == OK
        
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
        #TODO: Tell everyone that 201 is cor creates.
        return jsonify(Users=mappedUser),200 #200 == OK

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
        #TODO: Tell everyone that 201 is cor creates.
        return jsonify(Users=mappedUser),200 #200 == OK

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
            return jsonify(User=self.mapNewUserToDict(res)),201

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
        
        return jsonify(User=self.mapNewUserToDict(res)),201

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
        return None

    def markDashUserInactive(self, duid):
        """
        Marks a user as inactive in the database.

        Calls the UserDAO to deactivate a dashboard user's account. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            duid: The ID of the user that will be deactivated.
            
        Returns:
            A JSON containing all the user with the updated dashboard user.
        """
        return None

    def markDashUserActive(self, duid):
        """
        Marks a user as active in the database.

        Calls the UserDAO to activate a dashboard user's account. It then
        maps the result to a JSON that contains the desired record. That JSON 
        object is then returned.

        Args:
            duid: The ID of the user that will be activated.
            
        Returns:
            A JSON containing all the user with the updated dashboard user.
        """
        return None

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
        return None
