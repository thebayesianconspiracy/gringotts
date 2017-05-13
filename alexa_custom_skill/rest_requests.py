import json
import requests
from splitwise import Splitwise
from flask import render_template

timeOut= 2.0
client_id = "soumyadeep9@gmail.com"
consumer_key = '9avqAwEDHj08BTSWo4rbklFSH9kBkDGYJVIcLuok'
consumer_secret = 'nn93bOnzbVnTHodCep94BOOEEe4CO6vdkJKPbAZp'

retail_base_url = "https://retailbanking.mybluemix.net/banking/icicibank/"
debitcard_base_url = "https://debitcardapi.mybluemix.net/debit/icicibank/"
biller_base_url = "https://biller.mybluemix.net/biller/icicibank/"
upi_base_url = "https://upiservice.mybluemix.net/banking/icicibank/"
creditcard_base_url = "https://creditcardapi.mybluemix.net/banking/icicibank/"
pockets_base_url = "https://pocketsapi.mybluemix.net/rest/Card/"

billers = ["Electricity", "LPG", "Mobile", "Internet"]
creditCardTypes = ["MASTERCARD", "VISA", "PLATINUM", "SIGNATURE" ]

ERROR_TIMEOUT = -2
ERROR_LIST  = -1

def callGet(url, payload):
    try:
        response = requests.get(url, params=payload,  timeout=timeOut)
    except:
        return ERROR_TIMEOUT, {}
    json_data = response.json()
    return response.status_code, json_data

def getAccountBalance(token, account_no):
    payload = {'client_id': client_id, 'token': token, 'accountno': account_no}
    url = retail_base_url + "balanceenquiry"
    return callGet(url, payload)

def getAccountSummary(token, custid, account_no):
    payload = {'client_id': client_id, 'token': token, 'accountno': account_no, 'custid': custid }
    url = retail_base_url + "account_summary"
    return callGet(url, payload)

def getMiniStatement(token, account_no):
    payload = {'client_id': client_id, 'token': token, 'accountno': account_no}
    url = retail_base_url + "recenttransaction"
    return callGet(url, payload)

def getnDaysTransaction(token, account_no, days):
    payload = {'client_id': client_id, 'token': token, 'accountno': account_no, 'days': days }
    url = retail_base_url + "ndaystransaction"
    return callGet(url, payload)

def getTransactionsInterval(token, accountno, fromdate, todate):
    payload = {'client_id': client_id, 'token': token, 'accountno': account_no, 'fromdate': fromdate, 'todate': todate }
    url = retail_base_url + "transactioninterval"
    return callGet(url, payload)

def listPayee(token, custid):
    payload = {'client_id': client_id, 'token': token, 'custid': custid }
    url = retail_base_url + "listpayee"
    return callGet(url, payload)

def fundTransfer(token, srcAccount, destAccount, amount):
    payload = {'client_id': client_id, 'token': token, 'srcAccount': srcAccount, 'destAccount': destAccount, 'amt': amount }
    url = retail_base_url + "fundTransfer"
    return callGet(url, payload)

def authDebitCardDetails(token, custid, debit_card_no, cvv, expiry_date):
    payload = {'client_id': client_id, 'token': token, 'custid': custid, 'debit_card_no': debit_card_no, 'cvv' : cvv, 'expiry_date': expiry_date }
    url = debitcard_base_url + "authDebitDetails"
    return callGet(url, payload)

def getBillerDetails(token, billername):
    payload = {'client_id': client_id, 'token': token, 'billername': billername }
    url = biller_base_url + "billerdetail"
    return callGet(url, payload)

def addBiller(token, billerdetail, state, custid, nickname, consumerno):
    payload = {'client_id': client_id, 'token': token, 'billerdetail': billerdetail, 'state': state, 'custid': custid, 'nickname': nickname, 'consumerno': consumerno }
    url = biller_base_url + "addbiller"
    return callGet(url, payload)

def checkBill(billName):
    return billTypes[billName]['amount']

def payBill(billName):
    payload = {'client_id': client_id, 'token': token, 'nickname': billTypes[billName]['nickname'], 'amount': billTypes[billName]['amount'], 'custid': custid }
    url = biller_base_url + "billpay"
    return callGet(url, payload)

def createVPA(token, accountNo, vpa):
    payload = {'client_id': client_id, 'token': token, 'accountNo': accountNo, 'vpa': vpa }
    url = upi_base_url + "createVPA"
    return callGet(url, payload)

def upiFundTransferVtoV(token, payerCustId, payerVPA, payeeVPA, amount, remarks):
    payload = {'client_id': client_id, 'token': token, 'payerCustId': payerCustId, 'payerVPA': payerVPA, 'payeeVPA': payeeVPA, 'amount': amount, 'remarks': remarks }
    url = upi_base_url + "upiFundTransferVToV"
    return callGet(url, payload)

def upiFundTransferVtoA(token, payerCustId, payerVPA, payeeAccount, amount, remarks):
    payload = {'client_id': client_id, 'token': token, 'payerCustId': payerCustId, 'payerVPA': payerVPA, 'payeeAccount': payeeAccount, 'amount': amount, 'remarks': remarks }
    url = upi_base_url + "upiFundTransferVToA"
    return callGet(url, payload)

def addCreditCard(token, custId, cardType, cardNo, expDate, cvvNo):
    if cardType not in creditCardTypes:
        return ERROR_LIST, {}
    payload = {'client_id': client_id, 'token': token, 'custId': custId, 'cardType': cardType, 'cardNo': cardNo, 'expDate': expDate, 'cvvNo': cvvNo }
    url = creditcard_base_url + "addCreditCard"
    return callGet(url, payload)

def getCreditCardDetails(token, cardNumber):
    payload = {'client_id': client_id, 'authToken': token, 'cardNumber': cardNumber }
    url = pockets_base_url + "getCardDetails"
    return callGet(url, payload)

def getSplitWiseBalance(access_token):
    if access_token is not None:
        sObj = Splitwise(consumer_key,consumer_secret)
        sObj.setAccessToken(access_token)
        status_code = 200
        friends = sObj.getFriends()
        owedSum = 0
        oweSum = 0
        for friend in friends:
            for balance in friend.getBalances():
                if float(balance.getAmount()) > 0:
                    owedSum = owedSum + float(balance.getAmount())
                elif float(balance.getAmount()) < 0:
                    oweSum = oweSum + float(balance.getAmount())
        payload = {'owedShare': owedSum, 'oweShare': oweSum }
    else:
        status_code = 400
        payload = {"error" : "can not access splitwise data"}
    return status_code, payload

def getMaxFriendOwed(access_token):
    sObj = Splitwise(consumer_key,consumer_secret)
    sObj.setAccessToken(access_token)
    friends = sObj.getFriends()
    maxSum = 0
    maxFriend = ''
    for friend in friends:
        for balance in friend.getBalances():
            if balance.getAmount() > maxSum:
                maxSum = balance.getAmount()
                maxFriend = friend.getFirstName()
    #print "Max friend " + maxFriend + " Max Balance " + maxSum
    status_code = 200
    payload = {'friend': maxFriend, 'amount': float(maxSum) }
    return status_code, payload


def authFunct(funct, args, name, amount_passed):
    if funct=='transfer':
        response = upiFundTransferVtoV(*args)
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
        response = payBill(*args)
        if (response[0] == 200):
            amount = rest.checkBill(billName)
            print "billName " + billName
            speech_text = render_template('pay_bill_response', billName=name, billAmount=amount)
            
        else:
            speech_text = render_template('icici_error')
        return speech_text

billTypes = {
    "electricity" : {
        "billerdetail" : "Electricity Board",
        "state" : "GUJARAT",
        "nickname" : "ece",
        "consumerno" : "90345672",
        "amount" : 1000,
        },
    "LPG" : {
        "billerdetail" : "HP",
        "state" : "GUJARAT",
        "nickname" : "gas",
        "consumerno" : "90345672",
        "amount" : 400,
        },
    "mobile" : {
        "billerdetail" : "Vodafone",
        "state" : "GUJARAT",
        "nickname" : "mob",
        "consumerno" : "9916733098",
        "amount" : 675,
        },
    "internet" : {
        "billerdetail" : "Reliance Jio",
        "state" : "GUJARAT",
        "nickname" : "net",
        "consumerno" : "90345672",
        "amount" : 1250,
        },
}



token = "e2e960794d44"
account_no = "4444777755551369"
custid = "33336369"
days = 2
fromdate = "2017-03-01"
todate = "2017-03-10"

srcAccount = account_no
destAccount = "4444777755551370"
amount = "1000"
debit_card_no = "3477551166996369"
cvv = "871"
expiry_date = "10-19"


vpa = "soumyadeep@icici"

payerCustId = custid
payerVPA = vpa
payeeVPA = "aditya@icici"
remarks = "splitwise"
payeeAccount = destAccount

cardType = creditCardTypes[0]
cardNo = "1234567898765432"
expDate = "10-19"
cvvNo = "081"

def testAll():
    status, json = getAccountBalance(token, account_no)
    print status, json
    status, json = getAccountSummary(token, custid, account_no)
    print status
    status, json = getMiniStatement(token, account_no)
    print status
    status, json = getnDaysTransaction(token, account_no, days)
    print status
    status, json = getTransactionsInterval(token, account_no, fromdate, todate)
    print status
    status, json = listPayee(token, custid)
    print status
    status, json = fundTransfer(token, srcAccount, destAccount, amount)
    print status
    status, json = authDebitCardDetails(token, custid, debit_card_no, cvv, expiry_date)
    print status
    status, json = getBillerDetails(token, billername)
    print status, json
    status, json = addBiller(token, billerdetail, state, custid, nickname, consumerno)
    print status, json
    status, json = payBill(token, custid, nickname, amount)
    print status, json
    status, json = createVPA(token, account_no, vpa)
    print status
    status, json = upiFundTransferVtoV(token, payerCustId, payerVPA, payeeVPA, amount, remarks)
    print status
    status, json = upiFundTransferVtoA(token, payerCustId, payerVPA, payeeAccount, amount, remarks)
    print status
    status, json = addCreditCard(token, custid, cardType, cardNo, expDate, cvvNo)
    print status
    status, json = getCreditCardDetails(token, cardNo)
    print status


#btype = "electricity"
#billerdetail = billTypes[btype]['billerdetail']
#state = billTypes[btype]['state']
#nickname = billTypes[btype]['nickname']
#consumerno = billTypes[btype]['consumerno']
#testAll()

def testOne():
    #status, json = getBillerDetails(token,"Internet")
    #status, json = payBill(token, custid, nickname, amount)
    #status, json = addBiller(token, billerdetail, state, custid, nickname, consumerno)
    status, json = payBill(token,custid, nickname, amount)
    

    print status, json
    
#testOne()


