from config.fb_config import fb_config
from firebase import Firebase

rtdb = Firebase(fb_config).database()
print(rtdb.child("v1").get().val())