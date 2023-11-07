import json
import discord
import responses
import requests


def read_balances():
    try:
        with open('balances.json', 'r') as file:
            balances = json.load(file)
        return balances
    except FileNotFoundError:
        return {}
    except json.decoder.JSONDecodeError:
        print("Error: Invalid JSON content in balances.json")
        return {}

def write_balances(balances):
    with open('balances.json', 'w') as file:
        json.dump(balances, file)

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)



def run_discord_bot():
    TOKEN = 'YOUR DISCORD TOKEN'
    intents = discord.Intents.default()
    intents.message_content = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content.strip())
        channel = str(message.channel)

        print(f"{username} said: '{user_message}' ({channel})")

        if user_message.lower() == '!balance':
            #user_id = str(message.author.id)
            
            balances = read_balances()
            if username not in balances:
                balances[username] = {"balance": 100000, "btc_coins": 0, "eth_coins": 0}
                write_balances(balances)
                await message.channel.send(f'Initial balance of $100,000 assigned to {message.author.mention}')
            else:
                current_balance = balances[username]["balance"]
                btc_coins = balances[username]["btc_coins"]
                eth_coins = balances[username]["eth_coins"]
                await message.channel.send(f'{message.author.mention}, your current balance is $ {current_balance} \n{btc_coins} BTC , \n{eth_coins} ETH.')


        elif user_message.lower().startswith('!buy'):
            _, symbol, purchase_amount = user_message.split()
            purchase_amount = int(purchase_amount)
            symbol = symbol.lower()
            
            if symbol == 'btc' or symbol == 'bitcoin':
                balances = read_balances()
                if username in balances and balances[username]["balance"] >= purchase_amount:
                    #get price
                    request_btc_price = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
                    data = request_btc_price.json()
                    btc_price = int(data['bitcoin']['usd'])
                    coin = purchase_amount/btc_price
                    #operation
                    balances[username]["balance"] -= purchase_amount
                    balances[username]["btc_coins"] += coin   
                    write_balances(balances)
                    #send message
                    await message.channel.send(f'{username} have bought {coin} BTC, worth {purchase_amount}, at price {btc_price}')
                    await message.channel.send(f'{username} current balance is $ {balances[username]["balance"]} and you own {balances[username]["btc_coins"]} BTC.')

                elif username in balances and balances[username]["balance"] < purchase_amount:
                    await message.channel.send("You don't have enough balance to purchase")
                else :
                    await message.channel.send("Please create account by typing !balance")
            elif symbol == 'eth' or symbol == 'ethereum':
                balances = read_balances()
                if username in balances and balances[username]["balance"] >= purchase_amount:
                    #get price
                    request_eth_price = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
                    data = request_eth_price.json()
                    eth_price = int(data['ethereum']['usd'])
                    coin = purchase_amount/eth_price
                    #operation
                    balances[username]["balance"] -= purchase_amount
                    balances[username]["eth_coins"] += coin   
                    write_balances(balances)
                    #send message
                    await message.channel.send(f'{username} have bought {coin} ETH, worth {purchase_amount}, at price {eth_price}')
                    await message.channel.send(f'{username} current balance is $ {balances[username]["balance"]} and you own {balances[username]["eth_coins"]} ETH.')

                elif username in balances and balances[username]["balance"] < purchase_amount:
                    await message.channel.send("You don't have enough balance to purchase")
                else :
                    await message.channel.send("Please create account by typing !balance")

        elif user_message.lower().startswith('!sell'):
            _, symbol, sell_amount = user_message.split()
            sell_amount = int(sell_amount)
            symbol = symbol.lower()

            if symbol == 'btc' or symbol == 'bitcoin':
                balances = read_balances()
                #get price
                request_btc_price = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd')
                data = request_btc_price.json()
                btc_price = int(data['bitcoin']['usd'])
                coin = sell_amount/btc_price
                if username in balances and balances[username]["btc_coins"] >= coin:
                    #operation
                    balances[username]["balance"] += sell_amount
                    balances[username]["btc_coins"] -= coin
                    write_balances(balances)
                    #send message
                    await message.channel.send(f'{username} have sold {coin} BTC, worth {sell_amount}, at price {btc_price}')
                    await message.channel.send(f'{username} current balance is $ {balances[username]["balance"]} and you own {balances[username]["btc_coins"]} BTC.')

                elif username in balances and balances[username]["btc_coins"] < coin:
                    await message.channel.send("You don't have enough coin to sell")
                else:
                    await message.channel.send("Please create account by typing !balance")

            elif symbol == 'eth' or symbol =='ethereum':
                balances = read_balances()
                #get price
                request_eth_price = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd')
                data = request_eth_price.json()
                eth_price = int(data['ethereum']['usd'])
                coin = sell_amount/eth_price
                if username in balances and balances[username]["eth_coins"] >= coin:
                    #operation
                    balances[username]["balance"] += sell_amount
                    balances[username]["eth_coins"] -= coin
                    write_balances(balances)
                    #send message
                    await message.channel.send(f'{username} have sold {coin} ETH, worth {sell_amount}, at price {eth_price}')
                    await message.channel.send(f'{username} current balance is $ {balances[username]["balance"]} and you own {balances[username]["eth_coins"]} ETH.')

                elif username in balances and balances[username]["eth_coins"] < coin:
                    await message.channel.send("You don't have enough coin to sell")
                else:
                    await message.channel.send("Please create account by typing !balance")


        #if user_message[0] == '?':
            ##await send_message(message, user_message, is_private=True)
        #else:
        else :
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)

