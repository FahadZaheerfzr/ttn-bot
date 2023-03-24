from requests import Session
import json
import config


def getInfo (): # Function to get the info
    url = config.API_URL

    parameters = { 'slug': 'bnb,titan-coin', 'convert': 'USD' } # API parameters to pass in for retrieving specific cryptocurrency data

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': config.API_KEY
    } # Replace 'YOUR_API_KEY' with the API key you have recieved in the previous step

    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)

    info = json.loads(response.text)
    prices ={
        'bnb_price': info['data']['1839']['quote']['USD']['price'],
        'ttn_price': info['data']['3913']['quote']['USD']['price']
    }
    return prices
        
