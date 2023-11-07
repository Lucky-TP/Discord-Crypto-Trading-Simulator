import requests

def get_btc_price() -> str:
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
        data = response.json()
        btc_price = data['bitcoin']['usd']
        return f'Current BTC price: ${btc_price}'
    except Exception as e:
        return f'Error fetching BTC price: {str(e)}'

def get_eth_price() -> str:
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
        data = response.json()
        eth_price = data['ethereum']['usd']
        return f'Current ETH price: ${eth_price}'
    except Exception as e:
        return f'Error fetching ETH price: {str(e)}'

def handle_response(message) -> str:
    p_message = message.lower()

    if p_message == 'hello' or p_message == 'hi':
        return 'Hi, this is crypto trading simulator'
    
    if p_message == 'btc price' :
        return get_btc_price()
    
    if p_message == 'eth price' :
        return get_eth_price()

    if p_message == '!help' :
        return "!balance to make account and check for current balance\n!buy btc 1000 for buying 1000 usd of btc\n!sell btc 1000 for selling 1000 usd of btc"

    return "You could use !help"