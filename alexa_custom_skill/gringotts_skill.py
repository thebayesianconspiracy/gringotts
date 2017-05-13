import logging
import json
import sys
import socket, re, os, sys, inspect
from flask import Flask, render_template, redirect, url_for
from flask import request as request_flask
from flask import session as session_flask
from flask_ask import Ask, request, session, question, statement, dialog
import rest_requests as rest
from splitwise import Splitwise
import datetime
import copy, random
app = Flask(__name__)
ask = Ask(app, "/")
app.secret_key = "test_secret_key"
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

token = "e2e960794d44"
account_no = "4444777755551369"
customer_id = "33336369"
consumer_key = '9avqAwEDHj08BTSWo4rbklFSH9kBkDGYJVIcLuok'
consumer_secret = 'nn93bOnzbVnTHodCep94BOOEEe4CO6vdkJKPbAZp'

questions = [["Who's your favourite actor?","brad Pitt"],
             ["What's your favourite sport?", 'basketball'],
             ["What's your favourite animal?","lion"],
             ["What's your favourite color?","black"]]
payee_details = {
                'sam' : '4444777755551370',
                'nick' : '4444777755551371',
                'john' : '4444777755551372',
                }
vpa_details = {
                'sam' : 'sam@icicibank',
                'nick' : 'nick@icicibank',
                'john' : 'john@icicibank',
                }
@ask.launch
def launch():
    speech_text = render_template('welcome')
    return question(speech_text).reprompt(speech_text).simple_card('GringottsResponse', speech_text)



#Done
@ask.intent('BalanceIntent')
def getAccountBalance():
    response = rest.getAccountBalance(token, account_no)
    if (response[0] == 200):
        print response[1][1]
        speech_text = render_template('balance_response', balance=response[1][1]['balance'])
    else:
        speech_text = render_template('icici_error')
    return statement(speech_text).simple_card('GringottsResponse', speech_text)


#Later
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


#Later
@ask.intent('SplitwiseBalanceIntent')
def splitwiseBalance():
    if 'access_token' in session_flask:
        print session_flask['access_token']
        response = rest.getSplitWiseBalance(session_flask['access_token'])
        print response
        speech_text = render_template('splitwise_balance_response', owe=response['owe'], owed=response['owed'])
        return question(speech_text)
    else:
        speech_text = render_template('splitwise_login_response')
        url = "http://" + socket.gethostbyname(socket.gethostname()) + ":5000/splitwise"
        return statement(speech_text).standard_card(title="splitwise login", text=speech_text + " " + url)


#Later
@ask.intent('SplitwiseMaxOweIntent')
def splitwiseMaxOwe():
    speech_text = render_template('splitwise_max_owe_response')
    return question(speech_text)

@ask.intent('MoneySpentIntent',
            mapping={'recent_duration' : 'RECENT_DURATION'})


#Done
def getMoneySpent(recent_duration):
    if recent_duration is not None:
        duration = re.search('\d+', recent_duration).group(0)
        response = rest.getnDaysTransaction(token, account_no, duration)
        print "getting data for days " + duration
        if (response[0] == 200):
            print response[1]
            if("message" in response[1][0]):
                if (response[1][0]["message"] == "No Data Found"):
                    amount = 0
            else:
                amount = 0
                for key in response[1][1:]:
                    if(key['credit_debit_flag'] == "Dr."):
                        amount = amount + float(key['transaction_amount'])
            speech_text = render_template('money_spent_response', amount=str(amount), duration=duration)
        else:
            speech_text = render_template('icici_error')
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        return dialog().dialog_directive()



#Done
@ask.intent('AuthQ', mapping={})
def CheckAuth():
    qa = random.choice(questions)
    print "question : " + qa[0]

    session.attributes['authorized'] = 0
    speech_text = render_template('ask_q', q = qa[0])
    session.attributes['current_question'] = qa[0]
    session.attributes['current_answer'] = qa[1]
    return question(speech_text).simple_card('GringottsResponse', speech_text)

#Now
@ask.intent('AuthA',mapping={'answer1':'AUTH_A_ONE','answer2':'AUTH_A_TWO','answer3':'AUTH_A_THREE','answer4':'AUTH_A_FOUR' })
def AnswerOne(answer1,answer2,answer3,answer4):
    print answer1,answer2,answer3,answer4
    print 'stored_asnwer' + session.attributes['current_answer']
    if(answer1=="None"):
        if(answer2=="None"):
            if(answer3=="None"):
                answer = answer4
            else:
                answer = answer3
        else:
            answer = answer2
    else:
        answer = answer1
    print answer
    if (answer == session.attributes['current_answer']):
        print "Correct Answer"
        speech_text = render_template('auth_verified')
        session.attributes['authorized'] = 1
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('auth_error')
        return statement(speech_text).simple_card('GringottsResponse', speech_text)

#Done
@ask.intent('TransferIntent', mapping={'payeeName':'PAYEE_NAME', 'payeeAmount' : 'PAYEE_AMOUNT'})
def transferMoney(recentDays, payeeName, payeeAmount):
    if payeeName is not None and payeeAmount is not None:
            print "payeeName - %s payeeAmount - %s" % (payeeName, payeeAmount)
            response = rest.upiFundTransferVtoV(token, customer_id, "soumyadeep@icicibank", vpa_details.get(payeeName.lower()), payeeAmount, "remarks")
            if (response[0] == 200):
                print response[1]
                try:
                    if (response[1][1]["status"] == "SUCCESS"):
                        speech_text = render_template('transfer_response', payeeName=payeeName, payeeAmount=payeeAmount)
                    else:
                        speech_text = render_template('transfer_error')
                except (KeyError, IndexError):
                    speech_text = render_template('transfer_error')
            return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        return dialog().dialog_directive()

#Done
@ask.intent('AddPayeeIntent',
            mapping={'payeeName': 'PAYEE_NAME', 'payeeVPA' : 'PAYEE_VPA'})
def addPayee(payeeName, payeeVPA):
    if payeeName is not None and payeeVPA is not None:
        payeeName = payeeName.lower();
        payeeVPA = payeeVPA.lower();
        print "payee name %s payeeVPA %s" % (payeeName, payeeVPA)
        if payee_details.get(payeeName):
            response = rest.createVPA(token, payee_details.get(payeeName), payeeVPA.replace(" at ", "@"))
            if (response[0] == 200):
                print response[1]
                try:
                    if (response[1][1]["response"].find("mapped successfully")) :
                        speech_text = render_template('add_payee_response', payeeName=payeeName, payeeVPA=payeeVPA)
                    else:
                        speech_text = render_template('add_payee_api_error')
                except (KeyError, IndexError):
                    speech_text = render_template('add_payee_api_error')
        else:
            speech_text = render_template('add_payee_name_error')
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        return dialog().dialog_directive()

#Done
@ask.intent('PayBillIntent',
            mapping={'billName': 'BILL_NAME'})
def payBill(billName):
    if billName is not None:
        response = rest.payBill(billName)
        if (response[0] == 200):
            amount = rest.checkBill(billName)
            print "billName " + billName
            speech_text = render_template('pay_bill_response', billName=billName, billAmount=amount)
            return question(speech_text).simple_card('GringottsResponse', speech_text)
        else:
            speech_text = render_template('icici_error')
            return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('pay_bill_name_error')
        return question(speech_text).simple_card('GringottsResponse', speech_text)

#Done
@ask.intent('CheckBillIntent',
            mapping={'billName': 'BILL_NAME', 'billDate': 'BILL_DATE'})
def checkBilly(billName, billDate):
    amount = rest.checkBill(billName)
    if billName is not None:
        speech_text = render_template('check_bill_response', billName=billName, billAmount=amount, billDate=billDate)
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        speech_text = render_template('check_bill_name_error')
        return question(speech_text).simple_card('GringottsResponse', speech_text)

@ask.session_ended
def session_ended():
    return "", 200


@ask.intent('AMAZON.HelpIntent')
def help():
    help_text = render_template('help')
    help_reprompt = render_template('help_reprompt')
    return question(help_text).reprompt(help_reprompt)


@ask.intent('AMAZON.StopIntent')
def stop():
    bye_text = render_template('bye')
    return statement(bye_text)


@ask.intent('AMAZON.CancelIntent')
def cancel():
    bye_text = render_template('bye')
    return statement(bye_text)

@app.route("/splitwise")
def home():
    if 'access_token' in session_flask:
        return redirect(url_for("loggedin"))
    return render_template("home.html")

@app.route("/splitwise/login")
def login():

    sObj = Splitwise(consumer_key,consumer_secret)
    url, secret = sObj.getAuthorizeURL()
    session_flask['secret'] = secret
    return redirect(url)


@app.route("/splitwise/login/authorized")
def authorize():

    if 'secret' not in session_flask:
       return redirect(url_for("home"))

    oauth_token    = request_flask.args.get('oauth_token')
    oauth_verifier = request_flask.args.get('oauth_verifier')

    sObj = Splitwise(consumer_key,consumer_secret)
    access_token = sObj.getAccessToken(oauth_token,session_flask['secret'],oauth_verifier)
    session_flask['access_token'] = access_token

    return redirect(url_for("loggedin"))


@app.route("/splitwise/loggedin")
def loggedin():
    if 'access_token' not in session_flask:
       return redirect(url_for("home"))

    print rest.getMaxFriendOwed(session_flask['access_token'])
    print rest.getSplitWiseBalance(session_flask['access_token'])
    return render_template("loggedin.html")

@app.route('/splitwise/logout')
def logout():
    session_flask.pop('access_token', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    #print rest.getAccountSummary(token, 33336369, account_no)
    #print rest.listPayee(token, 33336369)
    #print rest.createVPA(token, account_no, "soumyadeep@icicibank")
    app.run(threaded=True,debug=True)
