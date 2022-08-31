import requests
from django.conf import settings

import json
def convert_currency(amount, curr_from, curr_to):

    url = f"https://api.apilayer.com/exchangerates_data/convert?to={curr_to}&from={curr_from}&amount={amount}"

    payload = {}
    headers= {
    "apikey": 'wS55XguJEzNOuWaCmBQ2sCLmLKtg2vge'
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    status_code = response.status_code
    result = json.loads(response.text)
    return result['result']
