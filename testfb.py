from functions import *

config = { #our config for our firebase app
    "apiKey": os.environ['FIREBASE_API_KEY'],
    "authDomain": os.environ['FIREBASE_AUTHDOMAIN'],
    "databaseURL": os.environ['FIREBASE_DATABASE_URL'],
    "storageBucket": os.environ['FIREBASE_STORAGE_BUCKET']
}

firebase = pyrebase.initialize_app(config) #initializes our firebase app, that can have database, auth, messaging etc.

auth = firebase.auth() #reference to the firebase app's authentication service
user = auth.sign_in_with_email_and_password(os.environ['FIREBASE_AUTH_EMAIL'], os.environ['FIREBASE_AUTH_PASSWORD']) # log the user of the database in

db = firebase.database() #grabbing the database in our firebase app

# storeUser("test",db,user)
# removeUser("1233625006706620",db,user)
print getAllUsers(db, user)