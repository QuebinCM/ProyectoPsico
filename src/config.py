import pyrebase

import firebase_admin
from firebase_admin import credentials, firestore

config = {
    "apiKey": "AIzaSyDocekuJ00lmQ08R9n7iQzRuNeXhvSecUU",
    "authDomain": "grielatest-50608.firebaseapp.com",
    "projectId": "grielatest-50608",
    "storageBucket": "grielatest-50608.appspot.com",
    "messagingSenderId": "788430879281",
    "appId": "1:788430879281:web:ebb90dc201004b2fce3310",
    "measurementId": "G-V4BC0V5DK4",
    'databaseURL': ''
}

cred = credentials.Certificate("src/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()