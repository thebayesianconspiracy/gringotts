import json
import requests


token = "bd8a9799dc54"
account_no = "4444777755551369"

def getAccountBalance(token, account_no):
    url = "https://retailbanking.mybluemix.net/banking/icicibank/balanceenquiry?client_id=soumyadeep9@gmail.com&token="
    url = url + token + "&accountno=" + account_no
    response = requests.get(url)
    json_data = json.loads(response.text)
    print json_data[1].get('balance')
    return json_data[1].get('balance')


#getAccountBalance(token,account_no)
