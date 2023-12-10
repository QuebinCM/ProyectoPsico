import pyrebase

import firebase_admin
from firebase_admin import credentials, firestore

config = {
    "apiKey": "AIzaSyCZHQUNhLO7sPDpLI5MmzyTzWWzWTQi1Og",
    "authDomain": "grielatest-23d0c.firebaseapp.com",
    "projectId": "grielatest-23d0c",
    "storageBucket": "grielatest-23d0c.appspot.com",
    "messagingSenderId": "22119078685",
    "appId": "1:22119078685:web:e8c26a4866c712ae4adff4",
    "measurementId": "G-0JZC4WG5LM",
    'databaseURL': ''
}

cred = credentials.Certificate("src/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()