import logging
import json
import sys
import os, sys, inspect
from flask import Flask
from flask_ask import Ask, request, session, question, statement

    

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    speech_text = 'Hi, I am Voice Pay'
    return question(speech_text).reprompt(speech_text).simple_card('GringottsResponse', speech_text)


@ask.intent('AccountSummaryIntent',
    mapping={'recentDays': 'RECENT_DAYS'})
def getAccountSummary(recentDays):
    speech_text = "You have no balance asshole"
    return statement(speech_text).simple_card('GringottsResponse', speech_text)


@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
