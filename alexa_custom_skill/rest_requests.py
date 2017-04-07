import json
import requests

client_id = "soumyadeep9@gmail.com"
retail_base_url = "aHR0cHM6Ly9yZXRhaWxiYW5raW5nLm15Ymx1ZW1peC5uZXQvYmFua2luZy9pY2ljaWJhbmsvCg=="
debitcard_base_url = "aHR0cHM6Ly9kZWJpdGNhcmRhcGkubXlibHVlbWl4Lm5ldC9kZWJpdC9pY2ljaWJhbmsvCg=="
biller_base_url = "aHR0cHM6Ly9iaWxsZXIubXlibHVlbWl4Lm5ldC9iaWxsZXIvaWNpY2liYW5rLwo="
upi_base_url = "aHR0cHM6Ly91cGlzZXJ2aWNlLm15Ymx1ZW1peC5uZXQvYmFua2luZy9pY2ljaWJhbmsvCg=="
creditcard_base_url = "aHR0cHM6Ly9jcmVkaXRjYXJkYXBpLm15Ymx1ZW1peC5uZXQvYmFua2luZy9pY2ljaWJhbmsvCg=="

def getAccountBalance(token, account_no):
    payload = {'client_id': client_id, 'token': token, 'accountno': account_no}
    url = retail_base_url + "balanceenquiry"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data
        
def getAccountSummary(token, cusid, account_no):
    payload = {'client_id': client_id, 'token': token, 'accountno': account_no, 'custid': custid }
    url = retail_base_url + "account_summary"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data
 
def getMiniStatement(token, account_no):
    payload = {'client_id': client_id, 'token': token, 'accountno': account_no}
    url = retail_base_url + "recenttransaction"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data
 
def getnDaysTransaction(token, account_no, days):
    payload = {'client_id': client_id, 'token': token, 'accountno': account_no, 'days': days }
    url = retail_base_url + "ndaystransaction"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data
     
def getTransactionsInterval(token, accountno, fromdate, todate):
    payload = {'client_id': client_id, 'token': token, 'accountno': account_no, 'fromdate': fromdate, 'todate': todate }
    url = retail_base_url + "transactioninterval"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data

def listPayee(token, custid):
    payload = {'client_id': client_id, 'token': token, 'custid': custid }
    url = retail_base_url + "listpayee"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data

def fundTransfer(token, srcAccount, destAccount, amount, payeeDesc, payeeId, type_of_transaction):
    payload = {'client_id': client_id, 'token': token, 'srcAccount': srcAccount, 'destAccount': destAccount, 'amt': amount, 'payeeDesc': payeeDesc, 'payeeId': payeeId, 'type_of_ransaction': type_of_transaction  }
    url = retail_base_url + "fundTransfer"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data

def authDebitCardDetails(token, custid, debit_card_no, cvv, expiry_date):
    payload = {'client_id': client_id, 'token': token, 'custid': custid, 'debit_card_no': debit_card_no, 'cvv' : cvv, 'expiry_date': expiry_date }
    url = debitcard_base_url + "authDebitDetails"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data

def getBillerDetails(token, billername):
    payload = {'client_id': client_id, 'token': token, 'billername': billername }
    url = base_url + "billerdetail"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data

def addBiller(token, billerdetail, state, custid, nickname, consumerno):
    payload = {'client_id': client_id, 'token': token, 'billerdetail': billerdetail, 'state': state, 'custid': custid, 'nickname': nickname, 'consumerno': consumerno }
    url = biller_base_url + "addbiller"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data

def payBill(token, custid, nickname, amount):
    payload = {'client_id': client_id, 'token': token, 'nickname': nickname, 'amount': amount }
    url = biller_base_url + "billpay"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data

def createVPA(token, accountNo, vpa):
    payload = {'client_id': client_id, 'token': token, 'accountNo': accountNo, 'vpa': vpa }
    url = upi_base_url + "createVPA"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data

def upiFundTransferVtoV(token, payerCustId, payerVPA, payeeVPA, amount, remarks):
    payload = {'client_id': client_id, 'token': token, 'payerCustId': payerCustId, 'payerVPA': payerVPA, 'payeeVPA': payeeVPA, 'amount': amount, 'remarks': remarks }
    url = upi_base_url + "upiFundTransferVtoV"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data

def upiFundTransferVtoA(token, payerCustId, payerVPA, payeeAccount, amount, remarks):
    payload = {'client_id': client_id, 'token': token, 'payerCustId': payerCustId, 'payerVPA': payerVPA, 'payeeAccount': payeeAccount, 'amount': amount, 'remarks': remarks }
    url = upi_base_url + "upiFundTransferVtoV"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data

def addCreditCard(token, custId, cardType, cardNo, expDate, cvvNo):
    payload = {'client_id': client_id, 'token': token, 'custId': custId, 'cardType': cardType, 'cardNo': cardNo, 'expDate': expDate, 'cvvNo': cvvNo }
    url = creditcard_base_url + "addCreditCard"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data

def getCreditCardDetails(token, cardNumber):
    payload = {'client_id': client_id, 'authToken': token, 'cardNumber': cardNumber }
    url = creditcard_base_url + "getCardDetails"
    response = requests.get(url, params=payload,  timeout=0.001)
    json_data = response.json()
    return response.status_code, json_data

def testAll():
    status, json = getAccountBalance(token, account_no)
    print status
    status, json = getAccountSummary(token, cusid, account_no)
    print status
    status, json = getMiniStatement(token, account_no)
    print status
    status, json = getnDaysTransaction(token, account_no, days)
    print status       
