from flask import jsonify
from handler.dao.user_dao import UserDAO
import json
import bcrypt
import jwt
import datetime



# BCrypt Authentication Related Functions

# Uses BCrypt hashing algorithm to hash a password given with
# the amount of rounds specified in the gensalt() method
# and returns the hash of the password.
def createHash(password):
    """
    Hashes the password of the user.

    Creates a hash of the password that is passed in, that way it is not
    stored as plaintext in the database.

    Args:
        password: The password to be hashed.

    Returns:
        hash: Returns the hashed password.
    """
    utfPasswd = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=10)  # 10 rounds for now
    hash = bcrypt.hashpw(utfPasswd, salt)

    return hash


def verifyHash(storedHash, password):
    """
    Verify the passed password's is a correct.

    Verifies the passed password matches the one stored in the database by
    comparing their hashes.

    Args:
        storedHash: The hash of the stored password.
        password: The password that's passed in the request.

    Returns:
        A boolean value signifying if the password is a match or not.
    """
    # hardcoding the user to be evaluated
    if storedHash == None:
        return False
    elif bcrypt.checkpw(password, storedHash.encode('utf-8')):
        return True
    else:
        return False


### JWT Token Related Functions ###


# Generates a new JWT token for the user with the secret key given and returns it.
def generateToken(username, key):
    """
      Creates a new token for the user.

      Generates a new token for the user in order to create an auth session.

      Args:
          username: The username of the user requesting the session.
          key: Secret key to sign the token.

      Returns:
          A valid token assigend to the provided user.
      """
    # Create a JWT token
    token = jwt.encode({'user': username, 'exp': datetime.datetime.utcnow(
    )+datetime.timedelta(minutes=3)}, key)
    return token.decode('UTF-8')


# Verifies a token with the key given.
def verifyToken(token, key):
    """
    Verify if the provided token is valid.

    Tkes the provided token and verifies it is valid.

    Args:
        token: The token provided by the user.
        key: Secret key to verify the token.

    Returns:
        A boolean value signifying if the token is valid or not.
    """
    try:
        jwt.decode(token, key), 403
        return True
    except:
        return False
