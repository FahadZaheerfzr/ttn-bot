from requests import Session
import requests
import config
import json


def getInfo():  # Function to get the info
    url = config.API_URL

    # API parameters to pass in for retrieving specific cryptocurrency data
    parameters = {'slug': 'bnb', 'convert': 'USD'}

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': config.API_KEY
    }  # Replace 'YOUR_API_KEY' with the API key you have recieved in the previous step

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    ttn_price = getTTNPrice()
    info = json.loads(response.text)
    prices = {
        'bnb_price': info['data']['1839']['quote']['USD']['price'],
        'ttn_price': ttn_price,
        'busd_price': 1,
    }
    return prices


def getTTNPrice():
    response = requests.get("https://api.geckoterminal.com/api/v2/networks/bsc/pools/0xc89f587cfe28c7a7cddf24cb0e6a125083c68f9e")
    result = response.json()
    return result['data']['attributes']['base_token_price_usd']



