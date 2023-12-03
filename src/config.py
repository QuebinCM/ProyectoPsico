import pyrebase

import firebase_admin
from firebase_admin import credentials, firestore

config = {
    "apiKey": "AIzaSyDO7Tgh8Y7jSv7cNvym4piCLYDEx9MiNUY",
    "authDomain": "grielatest-90a50.firebaseapp.com",
    "projectId": "grielatest-90a50",
    "storageBucket": "grielatest-90a50.appspot.com",
    "messagingSenderId": "161945135632",
    "appId": "1:161945135632:web:cc9a67b29ce447263fb895",
    "measurementId": "G-V4BC0V5DK4",
    'databaseURL': ''
}

cred = credentials.Certificate("src/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()