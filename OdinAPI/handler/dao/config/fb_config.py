# Import os library to determine CWD.
import os

# NOTE: Run from root directory (OdinAPI).

# Firebase RTBD Config.
fb_config = {
    'apiKey': "AIzaSyAOGsd_Hwr8QXnEz6ArC21WOnhUPw_bJAE",
    'authDomain': "mjolnir-pbp-v1.firebaseapp.com",
    'databaseURL': "https://mjolnir-pbp-v1.firebaseio.com",
    'storageBucket': "mjolnir-pbp-v1.appspot.com",
    'serviceAccount': os.getcwd() + "/handler/dao/config/mjolnir-pbp-v1-firebase-adminsdk-totsu-806dc7ce74.json"
}