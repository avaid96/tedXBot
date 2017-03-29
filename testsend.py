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

import requests
import sys, os, json

def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(
        recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(message):  # simple wrapper for logging to stdout on heroku
    print str(message)
    sys.stdout.flush()

users = getAllUsers(db, user)
for user in users:
    send_message(user, "abc")