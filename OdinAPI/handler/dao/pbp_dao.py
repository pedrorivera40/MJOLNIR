from config.fb_config import serv_path, rtdb_config
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class PBPDao:

    # Initialize Firebase Admin SDK and set Realtime Database instance.
    def __init__(self):
        firebase_admin.initialize_app(
            credentials.Certificate(serv_path), rtdb_config)
        self.rtdb = db


if __name__ == '__main__':

    # Initialize a Play-by-Play DAO for quick testing purposes.
    pbp_dao = PBPDao()
    print(pbp_dao.rtdb.reference("v1").get())
