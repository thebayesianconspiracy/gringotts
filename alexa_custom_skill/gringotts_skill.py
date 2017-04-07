import logging
import json
import sys
import os, sys, inspect
from flask import Flask
from flask_ask import Ask, request, session, question, statement
import rest_requests as rest


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

token = "f4773fe50e94"
account_no = "4444777755551369"

@ask.launch
def launch():
    speech_text = 'Hi, I am Voice Pay. How can I help?'
    return question(speech_text).reprompt(speech_text).simple_card('GringottsResponse', speech_text)


@ask.intent('BalanceIntent')
def getAccountBalance():
    response = rest.getAccountBalance(token, account_no)
    if response[0] == 200:
        balanceResponse = response[1]
        balanceValue = balanceResponse[1].get('balance')
        speech_text = "Your balance is " + balanceValue + " rupees"
    else:
        speech_text = "There was an error processing your request"
    return statement(speech_text).simple_card('GringottsResponse', speech_text)

@ask.intent('RecentTransactionsIntent',
    mapping={'recentDays': 'RECENT_DAYS', 'fromDay':'FROM_DAY', 'toDay' : 'TO_DAY'})
def getRecentTransactions(recentDays, fromDay, toDay):
    if recentDays is not None:
        print "recentDays " + recentDays
        speech_text = 'Your transactions in the last ' + str(recentDays) + ' days are'
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    elif fromDay is not None:
        print "fromDay " + fromDay
        speech_text = 'Your transactions in the last ' + str(fromDay) + ' days are'
    elif toDay is not None:
        print "toDay " + toDay
        speech_text = 'Your transactions in the last ' + str(toDay) + ' days are'
    else :
        speech_text = 'Please specify a duration'
        return question(speech_text).simple_card('GringottsResponse', speech_text)
    return statement("Error").simple_card('GringottsResponse', speech_text)

@ask.intent('MoneySpentIntent',
    mapping={'recentDays': 'RECENT_DAYS'})
def getMoneySpent(recentDays, fromDay, toDay):
    if recentDays is not None:
        print "recentDays " + recentDays
        speech_text = 'You have spent lot of money in the last ' + str(recentDays) + ' days'
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = 'Please specify a duration'
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    return statement("Error").simple_card('GringottsResponse', speech_text)

@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
