# Import os library to determine CWD.
import os

# Path to service account credentials.
serv_path = os.getcwd() + \
    "/handler/dao/config/white-smile-272204-firebase-adminsdk-spbxn-4ca34ac3ff.json"

# Firebase RTBD config information required by Firebase Admin SDK.
rtdb_config = {
    "databaseURL": "https://white-smile-272204.firebaseio.com/",
}
