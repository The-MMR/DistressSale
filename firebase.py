# firebase.py
import json
import os
import firebase_admin
from firebase_admin import credentials, firestore

# For local dev (if you're using a firebase-key.json file)
def init_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate("firebase-key.json")
        firebase_admin.initialize_app(cred)
    return firestore.client()
