import json
import requests

import wallet_cli
import pypayd

DEFAULT_TRX_TYPE = 'trx'


def get_trx_data_from_user() -> dict:
    recipient_pubkey = input("please enter recipient public key: ")
    transaction_amount = float(input("please enter transaction amount: "))
    trxfee_amount = float(input("enter trxfee amount(set 0 if you dont want to pay trxfee): "))
    trx_type = DEFAULT_TRX_TYPE

    return { 'recipient_pubkey' : recipient_pubkey,
    'amount' : transaction_amount,
    'trxfee_amount' : trxfee_amount,
    'trx_type' : trx_type}


def create_new_transaction(**kwargs):
    wallet = wallet_cli.wallet()
    transaction = wallet.create_transaction(**kwargs)
    return json.dumps(transaction, indent=4, sort_keys= True)


def send_transaction_to_every_neighbour_node(transaction):
    print(transaction)
    neighbour_nodes_list = pypayd.deamon_node.relative_nodes
    successfull_request_count = 0
    
    for neighbour in neighbour_nodes_list:
        url = "http://" + neighbour + "/new-transaction"
        try:
            request = requests.post(url=url, json= transaction)

            if request.json().get("status") == 200:
                successfull_request_count += 1
            else:
                print(f"sending tranaction to node: {neighbour} failed, {request.json()}")
        except:
            pass
    
    if successfull_request_count < 1:
        print("transactions sending failed: no attempts were accepted")
    

if __name__ == "__main__":
    user_input = get_trx_data_from_user()
    jsonified_transaction = create_new_transaction(**user_input)
    send_transaction_to_every_neighbour_node(jsonified_transaction)