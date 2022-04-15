import json


def update(transactions_list:list, pubkey:str):
    with open('coins.json', 'r') as f:
        current_coins = json.load(f)

    for transaction in transactions_list:
        incoins = transaction.get('incoins')
        for coin in incoins:
            if current_coins.get(coin) is not None:
                del current_coins[coin]
        
        recipient = transaction.get('outcoins').get('recipient')
        sender = transaction.get('outcoins').get('sender')
        if sender.get('coin') is not None and sender.get('pubkey') == pubkey:
            coin_amount = float(sender.get('coin').split('Q')[2])
            current_coins[sender.get('coin')] = coin_amount
        
        elif recipient.get('pubkey') == pubkey:
            coin_amount = float(recipient.get('coin').split('Q')[2])
            current_coins[recipient.get('coin')] = coin_amount
    
    with open('coins.json', 'w') as f:
        json.dump(current_coins, f, indent=4)