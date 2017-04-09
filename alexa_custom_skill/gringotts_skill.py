import logging
import json
import sys
import random
import copy
import os, sys, inspect
from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement
import rest_requests as rest


questions = [["Who's your favourite actor?","Morgan freeman"],
             ["How old were you when you first went out of India?", '16']
            ]
            


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
        reprompt_text = render_template('recent_transaction_reprompt')
        speech_text = render_template('recent_transactions_range_error')
        return question(speech_text).reprompt(reprompt_text)

@ask.intent('TransferIntent',
    mapping={'payeeName':'PAYEE_NAME', 'payeeAmount' : 'PAYEE_AMOUNT'})
def transferMoney(recentDays, payeeName, payeeAmount):
    if payeeName is not None:
        if payeeAmount is not None:
            print "payeeName " + payeeName
            speech_text = render_template('transfer_response', payeeName=payeeName, payeeAmount=payeeAmount)
            return statement(speech_text).simple_card('GringottsResponse', speech_text)
        else:
            reprompt_text = render_template('transfer_amount_reprompt')
            speech_text = render_template('transfer_amount_error')
            return question(speech_text).reprompt(reprompt_text)
    else :
        reprompt_text = render_template('transfer_name_reprompt')
        speech_text = render_template('transfer_name_error')
        return question(speech_text).reprompt(reprompt_text)

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


@ask.intent('PayBillIntent',
    mapping={'billName': 'BILL_NAME'})
def payBill(billName):
    if billName is not None:
        print "billName " + billName
        speech_text = render_template('pay_bill_response', billName=billName, billAmount=100)
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('pay_bill_name_error')
        return question(speech_text).simple_card('GringottsResponse', speech_text)

@ask.intent('CheckBillIntent',
    mapping={'billName': 'BILL_NAME', 'billDate': 'BILL_DATE'})
def checkBill(billName, billDate):
    if billName is not None:
        if billDate is not None:
            print "billName " + billName + "billDate " + billDate
            speech_text = render_template('check_bill_response', billName=billName, billAmount=100, billDate=billDate)
            return statement(speech_text).simple_card('GringottsResponse', speech_text)
        else:
            print "billName " + billName + "billDate " + "this month"
            speech_text = render_template('check_bill_response', billName=billName, billAmount=100, billDate="this month")
            return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('check_bill_name_error')
        return question(speech_text).simple_card('GringottsResponse', speech_text)

@ask.intent('AddBillerIntent',
    mapping={'billName': 'BILL_NAME', 'billerName': 'BILLER_NAME'})
def checkBill(billName, billerName):
    if billName is not None:
        if billerName is not None:
            print "billName " + billName + "billerName " + billerName
            speech_text = render_template('add_biller_response', billName=billName, billerName=billerName)
            return statement(speech_text).simple_card('GringottsResponse', speech_text)
        else:
            print "billName " + billName
            speech_text = render_template('add_biller_name_error')
            return question(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('add_biller_bill_error')
        return question(speech_text).simple_card('GringottsResponse', speech_text)


@ask.intent('CheckAuth',
    mapping={})
def CheckAuth():
    ques_copy = copy.deepcopy(questions)
    q1 = random.choice(ques_copy)
    print "question : " + q1[0]
    
    session.attributes['authorized'] = 0
    speech_text = render_template('ask_q1', q1 = q1[0])
    session.attributes['current_question'] = q1[0]
    session.attributes['current_answer'] = q1[1]
    session.attributes['question_number'] = 1
    return question(speech_text).simple_card('GringottsResponse', speech_text)


@ask.intent('VerifyAuthQOne',
    mapping={'answer':'ANSWER_Q_ONE'})
def AnswerOne(answer):

    print 'answer' + answer
    print 'stored_asnwer' + session.attributes['current_answer']
    if (answer == session.attributes['current_answer']):
        print "Correct Answer"
        speech_text = render_template('auth_verified')
        session.attributes['authorized'] = 1
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('auth_error')
        return statement(speech_text).simple_card('GringottsResponse', speech_text)



@ask.intent('VerifyAuthQTwo',
    mapping={'answer':'ANSWER_Q_TWO'})
def AnswerOne(answer):
    print 'answer' + answer
    print 'stored_asnwer' + session.attributes['current_answer']
    if (answer == session.attributes['current_answer']):
        print "Correct Answer"
        speech_text = render_template('auth_verified')
        session.attributes['authorized'] = 1
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('auth_error')
        return statement(speech_text).simple_card('GringottsResponse', speech_text)




@ask.intent('VerifyAuthQThree',
    mapping={'answer':'ANSWER_Q_THREE'})
def AnswerOne(answer):

    print 'answer' + answer
    print 'stored_asnwer' + session.attributes['current_answer']
    if (answer == session.attributes['current_answer']):
        print "Correct Answer"
        speech_text = render_template('auth_verified')
        session.attributes['authorized'] = 1
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('auth_error')
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    


@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
