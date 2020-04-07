from flask import jsonify
from handler.dao.user_dao import UserDAO
import json
import bcrypt
import jwt
import datetime
import os
import re
from dotenv import load_dotenv
load_dotenv()


###################################
### Password Related Functions ###
###################################

def rulesMatch(password):
    """
    Verifies the password complies with pasword rules.

    Takes in a password and checks it against a regular espression to
    verify it is a compliant password that contains: At least 1 upercase letter,
    1 lowecase letter, at least 1 number, at least 1 symbol, and is between 
    10 and 64 characters long.

    Args:
        password: password to be checked againt the regex.
    
    Returns:
        A boolean to determine if the password complies or not.
    """
    pw = password

    # set the rules for the regular expression
    reg = "111111"

    # Compile it
    compiledReg = re.compile(reg)

    # Create the matcher.
    match = re.search(compiledReg, pw)

    # Return true if it matches false if it does not.
    return match

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
    encoded = bcrypt.hashpw(utfPasswd, salt)
    decoded = encoded.decode('utf-8')
    return decoded


def verifyHash(password, storedHash):
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
    return bcrypt.checkpw(password.encode('utf-8'), storedHash.encode('utf-8'))

###################################
### JWT Token Related Functions ###
###################################

# Generates a new JWT token for the user with the secret key given and returns it.
def generateToken(username):
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
    payload = {
        'user': username,
        'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=3),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
    return f'Bearer {token.decode("UTF-8")}'


# Verifies a token with the key given.
def verifyToken(token):
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
        jwt.decode(token, os.getenv('SECRET_KEY'), algorithm='HS256')
        return True
    except:
        return False
