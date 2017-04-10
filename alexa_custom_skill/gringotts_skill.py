import logging
import json
import sys
import os, sys, inspect
from flask import Flask, render_template
from flask_ask import Ask, request, session, question, statement
import rest_requests as rest
import datetime
import copy, random

app = Flask(__name__)
ask = Ask(app, "/")
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

token = "f4773fe50e94"
account_no = "4444777755551369"

questions = [["Who's your favourite actor?","brad Pitt"],
             ["How old were you when you first went out of India?", '16']
]

@ask.launch
def launch():
    speech_text = render_template('welcome')
    return question(speech_text).reprompt(speech_text).simple_card('GringottsResponse', speech_text)

@ask.intent('BalanceIntent')
def getAccountBalance():
    response = rest.getAccountBalance(token, account_no)
    speech_text = render_template('balance_response', balance=94563)
    return statement(speech_text).simple_card('GringottsResponse', speech_text)

@ask.intent('RecentTransactionsIntent',
            mapping={'fromDay':'FROM_DAY', 'toDay' : 'TO_DAY'}, default={'toDay': datetime.datetime.now().strftime ("%Y-%m-%d")  })
def getRecentTransactions(fromDay, toDay):
    session.attributes['root'] = 'transactions'
    if fromDay is not None:
        speech_text = render_template('recent_transactions_response', fromDay=fromDay, toDay=toDay)
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else:
        print "Question"
        reprompt_text = render_template('recent_transactions_reprompt')
        speech_text = render_template('recent_transactions_range_error')
        return question(speech_text).reprompt(reprompt_text)

@ask.intent('DurationIntent', mapping={'fromDay':'FROM_DAY', 'toDay':'TO_DAY'}, default={'toDay': datetime.datetime.now().strftime ("%Y-%m-%d")  })
def getDuration(fromDay, toDay):
    root = session.attributes['root']
    print root
    if root == 'transactions':
        if fromDay is not None:
            speech_text = render_template('recent_transactions_response', fromDay=fromDay, toDay=toDay)
            return statement(speech_text).simple_card('GringottsResponse', speech_text)
        else:
            reprompt_text = render_template('recent_transaction_reprompt')
            speech_text = render_template('recent_transactions_range_error')
            return question(speech_text).reprompt(reprompt_text)
    else:
        speech_text = render_template('wrong_intent_text')
        return statement(speech_text).simple_card('GringottsResponse', speech_text)

@ask.intent('SplitwiseBalanceIntent')
def splitwiseBalance():
    speech_text = render_template('splitwise_balance_response')
    return question(speech_text)

@ask.intent('SplitwiseMaxOweIntent')
def splitwiseMaxOwe():
    speech_text = render_template('splitwise_max_owe_response')
    return question(speech_text)

@ask.intent('MoneySpentIntent',
            mapping={'duration' : 'DURATION'}, default = { 'duration': 'P3D' })
def getMoneySpent(duration):
    if duration is not None:
        speech_text = render_template('money_spent_response', amount=3478, duration=duration)
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('money_spent_error')
        return statement(speech_text).simple_card('GringottsResponse', speech_text)

@ask.intent('YesIntent')
def getConfirmation():
#       if session.attributes['root'] == "paybillintent":
    speech_text = render_template('auth_yes')
    return question(speech_text).simple_card('GringottsResponse', speech_text)

@ask.intent('CheckAuth', mapping={})
def CheckAuth():
    ques_copy = copy.deepcopy(questions)
    q1 = ques_copy[0]
    print "question : " + q1[0]
    
    session.attributes['authorized'] = 0
    speech_text = render_template('ask_q1', q1 = q1[0])
    session.attributes['current_question'] = q1[0]
    session.attributes['current_answer'] = q1[1]
    session.attributes['question_number'] = 1
    return question(speech_text).simple_card('GringottsResponse', speech_text)


@ask.intent('VerifyAuthQOne',mapping={'answer':'ANSWER_Q_ONE'})
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

@ask.intent('VerifyAuthQTwo', mapping={'answer':'ANSWER_Q_TWO'})
def AnswerTwo(answer):
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
    

@ask.intent('VerifyAuthQThree',mapping={'answer':'ANSWER_Q_THREE'})
def AnswerThree(answer):
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

#TODO: Add intents for name and amount
@ask.intent('TransferIntent', mapping={'payeeName':'PAYEE_NAME', 'payeeAmount' : 'PAYEE_AMOUNT'})
def transferMoney(recentDays, payeeName, payeeAmount):
    if payeeName is not None:
        if payeeAmount is not None:
            print "payeeName " + payeeName
            speech_text = render_template('transfer_response', payeeName=payeeName, payeeAmount=payeeAmount)
            return question(speech_text).simple_card('GringottsResponse', speech_text)
        else:
            reprompt_text = render_template('transfer_amount_reprompt')
            speech_text = render_template('transfer_amount_error')
            return question(speech_text).reprompt(reprompt_text)
    else :
        reprompt_text = render_template('transfer_name_reprompt')
        speech_text = render_template('transfer_name_error')
        return question(speech_text).reprompt(reprompt_text)

#TODO: Add payee details
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

#TODO: Ask amount as response
@ask.intent('PayBillIntent',
            mapping={'billName': 'BILL_NAME'})
def payBill(billName):
    if billName is not None:
        print "billName " + billName
        speech_text = render_template('pay_bill_response', billName=billName, billAmount=678)
        return question(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('pay_bill_name_error')
        return question(speech_text).simple_card('GringottsResponse', speech_text)

#TODO: Does not exist
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

#TODO: Add biller details
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

@ask.session_ended
def session_ended():
    return "", 200


if __name__ == '__main__':
    app.run(debug=True)
