import os
import firebase_admin
from firebase_admin import credentials, firestore

def initialize_firebase():
    if not firebase_admin._apps:
        cred_path = os.path.join(os.path.dirname(__file__), 'credentials', 'testpython-673c0-firebase-adminsdk-fbsvc-cfdb9b6a07.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()
