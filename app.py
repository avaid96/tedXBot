import os
import sys
import json
from functions import *

import requests
from flask import Flask, request
import pyrebase

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

app = Flask(__name__)


@app.route('/blast', methods=['GET'])
def blastmessage():
    formdata = request.args
    users = getAllUsers(db, user)
    del users['1857053561207408']
    for eachuser in users:
        send_message(eachuser, formdata['message'])
    return 'OK', 200

@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello World", 200

@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                if messaging_event.get("message"):  # someone sent us a message

                    # the facebook ID of the person sending you the message
                    sender_id = messaging_event["sender"]["id"]
                    # the recipient's ID, which should be your page's facebook ID
                    recipient_id = messaging_event["recipient"]["id"]

                    message_text = messaging_event["message"]["text"]  # the message's text
                    if message_text=="unsubscribe":
                        send_message(sender_id, "done")
                    else:
                        searchLink=SearchTedx(message_text)
                        vidLink=getFirstLink(searchLink)
                        #get sender info
                        userInfo = getUserInfo(str(recipient_id))
                        #store user in firebase
                        storeUser(recipient_id,db,user)

                        send_message(sender_id, vidLink)

                if messaging_event.get("delivery"):  # delivery confirmation
                    pass

                if messaging_event.get("optin"):  # optin confirmation
                    pass

                # user clicked/tapped "postback" button in earlier message
                if messaging_event.get("postback"):
                    pass

    return "ok", 200


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


if __name__ == '__main__':
    app.run(debug=True)
