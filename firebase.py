import os
import json
from firebase_admin import credentials, initialize_app, firestore

def init_firebase():
    if not firebase_admin._apps:
        key_dict = json.loads(os.environ["FIREBASE_KEY"])
        cred = credentials.Certificate(key_dict)
        initialize_app(cred)
    return firestore.client()
