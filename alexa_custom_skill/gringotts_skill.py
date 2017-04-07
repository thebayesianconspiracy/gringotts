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
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    elif toDay is not None:
        print "toDay " + toDay
        speech_text = 'Your transactions in the last ' + str(toDay) + ' days are'
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = 'Please specify a duration'
        return question(speech_text).simple_card('GringottsResponse', speech_text)
    return statement("Error").simple_card('GringottsResponse', speech_text)

@ask.intent('TransferIntent',
    mapping={'payeeName':'PAYEE_NAME', 'payeeAmount' : 'PAYEE_AMOUNT'})
def transferMoney(recentDays, payeeName, payeeAmount):
    if payeeName is not None:
        if payeeAmount is not None:
            print "payeeName " + payeeName
            speech_text = 'I transferred ' + str(payeeAmount) + ' to ' + payeeName
            return statement(speech_text).simple_card('GringottsResponse', speech_text)
        else:
            speech_text = 'Please specify amount'
            return question(speech_text).simple_card('GringottsResponse', speech_text)    
    else :
        speech_text = 'Please repeat name'
        return question(speech_text).simple_card('GringottsResponse', speech_text)
    return statement("Error").simple_card('GringottsResponse', speech_text)

@ask.intent('MoneySpentIntent',
    mapping={'recentDays': 'RECENT_DAYS', 'recentDuration' : 'RECENT_DURATION'})
def getMoneySpent(recentDays, recentDuration):
    if recentDays is not None:
        print "recentDays " + recentDays
        speech_text = 'You have spent lot of money in the last ' + str(recentDays)
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    elif recentDuration is not None:
        print "recentDuration" + recentDuration
        speech_text = 'You have spent lot of money in the last ' + str(recentDuration) + ' days'
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = 'Please specify a duration'
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    return statement("Error").simple_card('GringottsResponse', speech_text)


@ask.intent('AddPayeeIntent',
    mapping={'payeeName': 'PAYEE_NAME'})
def addPayee(payeeName):
    if payeeName is not None:
        print "payee name " + payeeName
        speech_text = 'I have added ' + payeeName + ' as a payee.'
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = 'Specify name properly.'
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    return statement("Error").simple_card('GringottsResponse', speech_text)




@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
