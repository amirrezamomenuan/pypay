import json
from collections import OrderedDict

import Exceptions

class TRX_TYPES:
    trx = 'trx'
    selftrx = 'selftrx'
    trxfee = 'trxfee'

blocks = {}  ################################################
LAST_BLOCK_INDEX = 152415 ########################################## get_last_block_index()


def check_coins_count(validated_coins_count:int , coins_count:int , pubkey:str):
    if validated_coins_count != len(coins_count):
        raise Exceptions.CoinException(f"coin(s) does not belong to the pubkey of : {pubkey}")


def check_incoins(transaction: dict, coins_list: list, block_id: int):
    incoins = transaction.get("incoins")

    for coin in coins_list:
        if coin in incoins:
            transaction_id = transaction.get("metadata").get("id")
            error_message = f"coin is already consumed in transaction with id : {transaction_id} on block : {block_id}"
            raise Exceptions.DoubleSpendError(error_message)


def check_trxfee_incoins(transaction: dict, coins_list: list):
    transaction_incoins = transaction.get('incoins')
    for coin in coins_list:
        if coin in transaction_incoins:
            transaction_id = transaction.get("metadata").get("id")
            error_message = f"coin is already consumed in transaction with id : {transaction_id} as the transaction fee"
            raise Exceptions.DoubleSpendError(error_message)


def check_outcoins(transaction: dict, coins_list: list, pubkey):
    validated_coins_count = 0

    recipient_pubkey = transaction.get("outcoins").get("recipient").get("pubkey")
    trx_coin = transaction.get("outcoins").get("recipient").get("coin")

    sender_pubkey = transaction.get("outcoins").get("sender").get("pubkey")
    reverse_trx_coin = transaction.get("outcoins").get("recipient").get("coin")

    for coin in coins_list:
        if recipient_pubkey == pubkey and coin == trx_coin:
            validated_coins_count += 1
            continue

        if sender_pubkey == pubkey and reverse_trx_coin == coin:
            validated_coins_count += 1
            continue
    
    return validated_coins_count


def check_selftrx_outcoins(transaction:OrderedDict, coins_list:list, sender_pub_key:str) -> int:
    self_trx_coin = transaction.get("outcoins").get("recipient").get("coin")
    self_trx_pubkey = transaction.get("outcoins").get("recipient").get("pubkey")

    for coin in coins_list:
        if coin == self_trx_coin and sender_pub_key == self_trx_pubkey:
            return 1
    return 0


def check_trxfee_outcoins(transaction:OrderedDict, coins_list:list, sender_pub_key:str) -> int: 
    self_trx_coin = transaction.get("outcoins").get("recipient").get("coin")
    self_trx_pubkey = transaction.get("outcoins").get("recipient").get("pubkey")

    for coin in coins_list:
        if coin == self_trx_coin and sender_pub_key == self_trx_pubkey:
            return 1
    return 0


def validate_coin(coins:list, sender_pub_key:str) -> bool:
    """
    to solve double spending problem the only requirement is to check imcoins list
    so in this function we are ignoring outcoins
    """
    last_block_index = LAST_BLOCK_INDEX
    validated_coins_count = 0

    while last_block_index >= 0:
        block = blocks[last_block_index]
        block = json.loads(block)

        for trx in block.get("trxs"):
            trx = json.loads(trx)

            trx_status = trx.get("metadata").get("status")
            if trx_status == TRX_TYPES.trx:
                check_incoins(trx, coins, last_block_index)
                validated_coins_count += check_outcoins(trx, coins, sender_pub_key)

            elif trx_status == TRX_TYPES.selftrx:
                validated_coins_count += check_selftrx_outcoins(trx, coins, sender_pub_key)

            elif trx_status == TRX_TYPES.trxfee:
                check_trxfee_incoins()
                validated_coins_count += check_trxfee_outcoins(trx, coins, sender_pub_key)

        last_block_index -= 1
        