import logging
import json
import sys
import os, sys, inspect
from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement
import rest_requests as rest


app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

token = "f4773fe50e94"
account_no = "4444777755551369"

@ask.launch
def launch():
    speech_text = render_template('welcome')
    return question(speech_text).reprompt(speech_text).simple_card('GringottsResponse', speech_text)


@ask.intent('BalanceIntent')
def getAccountBalance():
    response = rest.getAccountBalance(token, account_no)
    if response[0] == 200:
        balanceResponse = response[1]
        balanceValue = balanceResponse[1].get('balance')
        speech_text = render_template('balance_response', balance=balanceValue)
    else:
        speech_text = render_template('request_process_error')
    return statement(speech_text).simple_card('GringottsResponse', speech_text)


@ask.intent('RecentTransactionsIntent',
    mapping={'recentDays': 'RECENT_DAYS', 'fromDay':'FROM_DAY', 'toDay' : 'TO_DAY'})
def getRecentTransactions(recentDays, fromDay, toDay):
    if recentDays is not None:
        print "recentDays " + recentDays
        speech_text = render_template('recent_transactions_response', recentDays=recentDays)
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    elif fromDay is not None:
        print "fromDay " + fromDay
        speech_text = render_template('recent_transactions_response', recentDays=fromDay)
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    elif toDay is not None:
        print "toDay " + toDay
        speech_text = render_template('recent_transactions_response', recentDays=toDay)
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('recent_transactions_range_error')
        return question(speech_text).simple_card('GringottsResponse', speech_text)

@ask.intent('TransferIntent',
    mapping={'payeeName':'PAYEE_NAME', 'payeeAmount' : 'PAYEE_AMOUNT'})
def transferMoney(recentDays, payeeName, payeeAmount):
    if payeeName is not None:
        if payeeAmount is not None:
            print "payeeName " + payeeName
            speech_text = render_template('transfer_response', payeeName=payeeName, payeeAmount=payeeAmount)
            return statement(speech_text).simple_card('GringottsResponse', speech_text)
        else:
            speech_text = render_template('transfer_amount_error')
            return question(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('transfer_name_error')
        return question(speech_text).simple_card('GringottsResponse', speech_text)

@ask.intent('MoneySpentIntent',
    mapping={'recentDays': 'RECENT_DAYS', 'recentDuration' : 'RECENT_DURATION'})
def getMoneySpent(recentDays, recentDuration):
    if recentDays is not None:
        print "recentDays " + recentDays
        speech_text = render_template('money_spent_response', amount=100, recentDays=str(recentDays))
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    elif recentDuration is not None:
        print "recentDuration" + recentDuration
        speech_text = render_template('money_spent_response', amount=100, recentDays=str(recentDuration))
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('recent_transactions_range_error')
        return statement(speech_text).simple_card('GringottsResponse', speech_text)


@ask.intent('AddPayeeIntent',
    mapping={'payeeName': 'PAYEE_NAME'})
def addPayee(payeeName):
    if payeeName is not None:
        print "payee name " + payeeName
        speech_text = render_template('add_payee_response', payeeName=payeeName)
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('add_payee_name_error')
        return statement(speech_text).simple_card('GringottsResponse', speech_text)

@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
