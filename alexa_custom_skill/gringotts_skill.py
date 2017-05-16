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
import paho.mqtt.client as paho


external_tokens={}

#broker = 'broker.hivemq.com'
#broker = '127.0.0.1'
broker = '13.126.2.187'
token = "e2e960794d44"
account_no = "4444777755551369"
customer_id = "33336369"
consumer_key = '9avqAwEDHj08BTSWo4rbklFSH9kBkDGYJVIcLuok'
consumer_secret = 'nn93bOnzbVnTHodCep94BOOEEe4CO6vdkJKPbAZp'
user_topic = "/text/" + customer_id + "/messages/user"
alexa_topic = "/text/" + customer_id + "/messages/alexa"
result_topic = "/text/" + customer_id + "/messages/result"
splitwise_server = 'https://b4ade4d1.ngrok.io/splitwise'

questions = [["Who's your favourite actor?","Angelina Jolie"],
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

app = Flask(__name__)
ask = Ask(app, "/")
app.secret_key = "test_secret_key"
logging.getLogger('flask_ask').setLevel(logging.DEBUG)

def on_connect(client, userdata, rc):
    print("Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.


def on_publish(client, userdata, mid):
    print("published : "+str(mid))

client = paho.Client(clean_session=True)
client.on_publish = on_publish
client.on_connect = on_connect

class Payload:
    slots = ""
    intent = ""
    text = ""
    customer_id = ""
    alexaData = ""
    def __init__(self, customer_id):
        self.customer_id = customer_id
    def setSlots(self,slots):
        self.slots = slots
    def setIntent(self,intent):
        self.intent = intent
    def setText(self,text):
        self.text = text
    def setAlexaData(self,alexaData):
        self.alexaData = alexaData


@ask.launch
def launch():
    speech_text = render_template('welcome')
    return question(speech_text).reprompt(speech_text).simple_card('GringottsResponse', speech_text)

#Done
@ask.intent('BalanceIntent')
def getAccountBalance():
    mqttPayload = Payload(customer_id)
    mqttPayload.setIntent('BalanceIntent')
    client.publish(user_topic, json.dumps(mqttPayload.__dict__), qos=0)
    response = rest.getAccountBalance(token, account_no)
    if (response[0] == 200):
        print response[1][1]
        speech_text = render_template('balance_response', balance=response[1][1]['balance'])
        mqttPayload.setAlexaData({'balance' : response[1][1]['balance']})
    else:
        speech_text = render_template('icici_error')
    mqttPayload.setText(speech_text)
    client.publish(alexa_topic, json.dumps(mqttPayload.__dict__), qos=0)
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


#Done
@ask.intent('SplitwiseBalanceIntent')
def splitwiseBalance():
    mqttPayload = Payload(customer_id)
    mqttPayload.setIntent('SplitwiseBalanceIntent')
    client.publish(user_topic, json.dumps(mqttPayload.__dict__), qos=0)
    if 'splitwise' in external_tokens:
        print external_tokens['splitwise'], 'yoyoyoyoyoyoy'
        response = rest.getSplitWiseBalance(external_tokens['splitwise'])
        print response
        if response[0]==200:
            speech_text = render_template('splitwise_balance_response', owe=(response[1]['oweShare']*(-1)), owed=response[1]['owedShare'])
        else:
            speech_text = render_template('splitwise_balance_error')
        mqttPayload.setText(speech_text)
        mqttPayload.setAlexaData({'oweShare' : (response[1]['oweShare']*(-1)), 'owedShare': response[1]['owedShare']})
        client.publish(alexa_topic, json.dumps(mqttPayload.__dict__), qos=0)
        return statement(speech_text)
    else:
        speech_text = render_template('splitwise_login_response')
        #url = "http://" + socket.gethostbyname(socket.gethostname()) + ":5000/splitwise"
        url = splitwise_server
        mqttPayload.setText(speech_text + " " + url)
        mqttPayload.setAlexaData({'login_url' : url})
        client.publish(alexa_topic, json.dumps(mqttPayload.__dict__), qos=0)
        return statement(speech_text).standard_card(title="splitwise login", text=speech_text + " " + url)


#Later
@ask.intent('SplitwiseMaxOweIntent')
def splitwiseMaxOwe():
    mqttPayload = Payload(customer_id)
    mqttPayload.setIntent('SplitwiseMaxOweIntent')
    client.publish(user_topic, json.dumps(mqttPayload.__dict__), qos=0)
    response = rest.getAccountBalance(token, account_no)
    if 'splitwise' in external_tokens:
        print external_tokens['splitwise']
        response = rest.getMaxFriendOwed(external_tokens['splitwise'])
        print response
        if response[0]==200:
            speech_text = render_template('splitwise_max_owe_response', owe=(response[1]['amount']*(-1)), friend=response[1]['friend'])
        else:
            speech_text = render_template('splitwise_balance_error')
        mqttPayload.setText(speech_text)
        mqttPayload.setAlexaData({'owe' : (response[1]['amount']*(-1)), 'friend' : response[1]['friend']})
        client.publish(alexa_topic, json.dumps(mqttPayload.__dict__), qos=0)
        return statement(speech_text)
    else:
        speech_text = render_template('splitwise_login_response')
        #url = "http://" + socket.gethostbyname(socket.gethostname()) + ":5000/splitwise"
        url = splitwise_server
        mqttPayload.setText(speech_text + " " + url)
        mqttPayload.setAlexaData({'login_url' : url})
        client.publish(alexa_topic, json.dumps(mqttPayload.__dict__), qos=0)
        return statement(speech_text).standard_card(title="splitwise login", text=speech_text + " " + url)


@ask.intent('MoneySpentIntent',
            mapping={'recent_duration' : 'RECENT_DURATION'})
#Done
def getMoneySpent(recent_duration):
    if recent_duration is not None:
        duration = re.search('\d+', recent_duration).group(0)
        mqttPayload = Payload(customer_id)
        mqttPayload.setIntent('MoneySpentIntent')
        mqttPayload.setSlots({'days' : duration})
        client.publish(user_topic, json.dumps(mqttPayload.__dict__), qos=0)
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
            mqttPayload.setAlexaData({'amount' : amount})
        else:
            speech_text = render_template('icici_error')
        mqttPayload.setText(speech_text)
        client.publish(alexa_topic, json.dumps(mqttPayload.__dict__), qos=0)
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        return dialog().dialog_directive()



#Done
@ask.intent('AuthQ', mapping={})
def CheckAuth():
    qa = random.choice(questions)
    print "question : " + qa[0]
    mqttPayload = Payload(customer_id)
    mqttPayload.setIntent('AuthQ')
    client.publish(user_topic, json.dumps(mqttPayload.__dict__), qos=0)
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
    if(answer1 is None):
        if(answer2 is None):
            if(answer3 is None):
                answer = answer4
            else:
                answer = answer3
        else:
            answer = answer2
    else:
        answer = answer1

    print answer
    mqttPayload = Payload(customer_id)
    mqttPayload.setIntent('AuthA')
    if (answer == session.attributes['current_answer']):
        print "Correct Answer"
        mqttPayloadResult = Payload(customer_id)
        mqttPayloadResult.setIntent(session.attributes['funct'])

        res = authFunct(session.attributes['funct'],session.attributes['args'], session.attributes['name'],session.attributes['amount'])
        session.attributes['authorized'] = 1

        response = rest.getAccountBalance(token, account_no)
        if (response[0] == 200):
            print response[1][1]
            text2 = render_template('balance_response', balance=response[1][1]['balance'])
            speech_text = render_template('auth_verified') + ' And ' + res + ' ' + text2
            if (session.attributes['funct'] == "transfer"):
                mqttPayloadResult.setAlexaData({'balance':response[1][1]['balance'],'name':session.attributes['name'],'amount':session.attributes['amount']});
            elif (session.attributes['funct'] == "paybill"):
                mqttPayloadResult.setAlexaData({'balance':response[1][1]['balance'],'name':session.attributes['name'],'amount':rest.checkBill(session.attributes['name'])});
        else:
            speech_text = render_template('auth_verified') + ' And ' + res
    else :
        speech_text = render_template('auth_error')
    mqttPayload.setText(speech_text)
    client.publish(alexa_topic, json.dumps(mqttPayload.__dict__), qos=0)
    if (session.attributes['funct'] == "transfer" or session.attributes['funct'] == "paybill"):
        client.publish(result_topic, json.dumps(mqttPayloadResult.__dict__), qos=0)
    return statement(speech_text).simple_card('GringottsResponse', speech_text)

@ask.intent('TransferIntent', mapping={'payeeName':'PAYEE_NAME', 'payeeAmount' : 'PAYEE_AMOUNT'})
def transferMoney(payeeName, payeeAmount):
    if payeeName is not None and payeeAmount is not None:
        payeeName = payeeName.lower();
        mqttPayload = Payload(customer_id)
        mqttPayload.setIntent('TransferIntent')
        mqttPayload.setSlots({'payeeName' : payeeName, 'payeeAmount' : payeeAmount})
        client.publish(user_topic, json.dumps(mqttPayload.__dict__), qos=0)
        print "payeeName - %s payeeAmount - %s" % (payeeName, payeeAmount)
        session.attributes['args'] = [token, customer_id, "soumyadeep@icicibank", vpa_details.get(payeeName), payeeAmount, "remarks"]
        session.attributes['funct'] = 'transfer'
        session.attributes['name'] = payeeName
        session.attributes['amount'] = payeeAmount
        speech_text = render_template('do_auth')
        mqttPayload.setText(speech_text)
        client.publish(alexa_topic, json.dumps(mqttPayload.__dict__), qos=0)
        return question(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        return dialog().dialog_directive()

@ask.intent('PayBillIntent',
            mapping={'billName': 'BILL_NAME'})
def payBill(billName):
    if billName is not None:
        mqttPayload = Payload(customer_id)
        mqttPayload.setIntent('PayBillIntent')
        mqttPayload.setSlots({'billName' : billName})
        client.publish(user_topic, json.dumps(mqttPayload.__dict__), qos=0)
        session.attributes['args'] = [billName]
        session.attributes['funct'] = 'paybill'
        session.attributes['name'] = billName
        session.attributes['amount'] = 0
        speech_text = render_template('do_auth')
        mqttPayload.setText(speech_text)
        client.publish(alexa_topic, json.dumps(mqttPayload.__dict__), qos=0)
        return question(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        return dialog().dialog_directive()

#Done
@ask.intent('AddPayeeIntent',
            mapping={'payeeName': 'PAYEE_NAME', 'payeeVPA' : 'PAYEE_VPA'})
def addPayee(payeeName, payeeVPA):
    if payeeName is not None and payeeVPA is not None:
        payeeName = payeeName.lower();
        payeeVPA = payeeVPA.lower();
        mqttPayload = Payload(customer_id)
        mqttPayload.setIntent('AddPayeeIntent')
        mqttPayload.setSlots({'payeeName' : payeeName, 'payeeVPA' : payeeVPA})
        client.publish(user_topic, json.dumps(mqttPayload.__dict__), qos=0)
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
        mqttPayload.setText(speech_text)
        mqttPayload.setAlexaData({'payeeName':payeeName, 'payeeVPA':payeeVPA})
        client.publish(alexa_topic, json.dumps(mqttPayload.__dict__), qos=0)
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        return dialog().dialog_directive()

#Done
@ask.intent('CheckBillIntent',
            mapping={'billName': 'BILL_NAME', 'billDate': 'BILL_DATE'})
def checkBilly(billName, billDate):
    if billName is not None and billDate is not None:
        mqttPayload = Payload(customer_id)
        mqttPayload.setIntent('CheckBillIntent')
        mqttPayload.setSlots({'billName' : billName, 'billDate' : billDate})
        client.publish(user_topic, json.dumps(mqttPayload.__dict__), qos=0)

        amount = rest.checkBill(billName)
        speech_text = render_template('check_bill_response', billName=billName, billAmount=amount, billDate=billDate)

        mqttPayload.setText(speech_text)
        mqttPayload.setAlexaData({'billName' : billName, 'billAmount' : amount, 'billDate' : billDate})
        client.publish(alexa_topic, json.dumps(mqttPayload.__dict__), qos=0)
        return statement(speech_text).simple_card('GringottsResponse', speech_text)
    else :
        return dialog().dialog_directive()


@ask.intent('CustomerCareIntent')
def initiateCustomerCare():
    mqttPayload = Payload(customer_id)
    mqttPayload.setIntent('CustomerCareIntent')
    client.publish(user_topic, json.dumps(mqttPayload.__dict__), qos=0)
    speech_text = render_template('customer_care_init')
    mqttPayload.setText(speech_text)
    client.publish(alexa_topic, json.dumps(mqttPayload.__dict__), qos=0)
    return question(speech_text).simple_card('GringottsResponse', speech_text)


@ask.intent('CardBlockIntent')
def blockCard():
    session.attributes['args'] = []
    session.attributes['funct'] = 'blockCard'
    session.attributes['name'] = ''
    session.attributes['amount'] = 0
    mqttPayload = Payload(customer_id)
    mqttPayload.setIntent('CardBlockIntent')
    client.publish(user_topic, json.dumps(mqttPayload.__dict__), qos=0)
    speech_text = render_template('do_auth')
    mqttPayload.setText(speech_text)
    client.publish(alexa_topic, json.dumps(mqttPayload.__dict__), qos=0)
    return question(speech_text).simple_card('GringottsResponse', speech_text)

@ask.intent('CCOptionIntent',mapping={'answer1':'OPTION_ONE','answer2':'OPTION_TWO','answer3':'OPTION_THREE','answer4':'OPTION_FOUR','answer5':'OPTION_FIVE' })
def AnswerOne(answer1,answer2,answer3,answer4,answer5):
    print answer1,answer2,answer3,answer4,answer5
    if(answer1 is None):
        if(answer2 is None):
            if(answer3 is None):
                if(answer4 in None):
                    answer = 'none'
                else:
                    answer = 'investments'
            else:
                answer = 'loans'
        else:
            answer = 'net_banking'
    else:
        answer = 'card'

    print answer
    mqttPayload = Payload(customer_id)
    mqttPayload.setIntent('CCOptionIntent')
    mqttPayload.setSlots({'answer' : answer})
    client.publish(user_topic, json.dumps(mqttPayload.__dict__), qos=0)
    speech_text = render_template('cc_'+answer)
    mqttPayload.setText(speech_text)
    client.publish(alexa_topic, json.dumps(mqttPayload.__dict__), qos=0)
    return question(speech_text).simple_card('GringottsResponse', speech_text)


def authFunct(funct, args, name, amount_passed):
    if funct=='transfer':
        response = rest.upiFundTransferVtoV(*args)
        if (response[0] == 200):
            print response[1]
            try:
                if (response[1][1]["status"] == "SUCCESS"):
                    speech_text = render_template('transfer_response', payeeName=name, payeeAmount=amount_passed)
                else:
                    speech_text = render_template('transfer_error')
            except (KeyError, IndexError):
                speech_text = render_template('transfer_error')
        else:
            speech_text = render_template('icici_error')
        return speech_text


    elif funct=='paybill':
        response = rest.payBill(*args)
        if (response[0] == 200):
            amount = rest.checkBill(name)
            print "billName " + name
            speech_text = render_template('pay_bill_response', billName=name, billAmount=amount)

        else:
            speech_text = render_template('icici_error')
        return speech_text

    elif funct=='blockCard':
        return(render_template('customer_care_block_card'))

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
    external_tokens['splitwise'] = access_token

    return redirect(url_for("loggedin"))


@app.route("/splitwise/loggedin")
def loggedin():
    if 'access_token' not in session_flask:
       return redirect(url_for("home"))

    external_tokens['splitwise'] = session_flask['access_token']
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
    try:
        client.connect(broker, 1883, 60)
        client.loop_start()
        print user_topic
        print alexa_topic
    except (KeyboardInterrupt, SystemExit):
        client.loop_stop()
        client.disconnect()

    app.run(threaded=True,debug=True)
