import json
from collections import OrderedDict

import Exceptions
import pypayd

class TRX_TYPES:
    trx = 'trx'
    selftrx = 'selftrx'
    trxfee = 'trxfee'

blocks = pypayd.chain.get_full_chain()
LAST_BLOCK_INDEX = pypayd.deamon_node.last_block_index


def check_coins_count(validated_coins_count:int , coins_count:int , pubkey:str) -> None:
    """
    this function is used to compare number of validated coins and 
    raises an error if number of coins and number of validated coins 
    are not equal
    """

    if validated_coins_count != len(coins_count):
        raise Exceptions.CoinException(f"coin(s) does not belong to the pubkey of : {pubkey}")


def check_incoins(transaction: dict, coins_list: list, block_id: int = 0, checks_ledger:bool = False) -> None:
    """
    this is a part of validating transaction where the incoins are checked
    to see if they were spend before

    there is a itteration in all transactions and if any of coins that are inside the current transaction
    are the same to past transaction incoins
    """

    incoins = transaction.get("incoins")

    for coin in coins_list:
        if coin in incoins:
            if checks_ledger:
                error_message = f"coin is already consumed in transaction located in ledger"
                raise Exceptions.DoubleSpendError(error_message)
            else:
                transaction_id = transaction.get("metadata").get("id")
                error_message = f"coin is already consumed in transaction with id : {transaction_id} on block : {block_id}"
                raise Exceptions.DoubleSpendError(error_message)


def check_trxfee_incoins(transaction: dict, coins_list: list) -> None:
    """
    this function checks to see if the coins in coins_list 
    are spend in other transactions as trxfee
    """

    transaction_incoins = transaction.get('incoins')
    for coin in coins_list:
        if coin in transaction_incoins:
            transaction_id = transaction.get("metadata").get("id")
            error_message = f"coin is already consumed in transaction with id : {transaction_id} as the transaction fee"
            raise Exceptions.DoubleSpendError(error_message)


def check_outcoins(transaction: dict, coins_list: list, pubkey):
    """
    this function will loop through every transaction (including mined ones and ledger transactions)
    and count the number of validated coins
    the mechanism works by checking if the incoins(coins_list) were given to
    the address with the pubkey(pubkey in input)
    """

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
    """
    checks if coin is mined and not generated in a normal transaction
    """

    self_trx_coin = transaction.get("outcoins").get("recipient").get("coin")
    self_trx_pubkey = transaction.get("outcoins").get("recipient").get("pubkey")

    for coin in coins_list:
        if coin == self_trx_coin and sender_pub_key == self_trx_pubkey:
            return 1
    return 0


def check_trxfee_outcoins(transaction:OrderedDict, coins_list:list, sender_pub_key:str) -> int: 
    """
    checks if coin is miners reward (as trxfee) and not generated in a normal transaction
    """
    
    self_trx_coin = transaction.get("outcoins").get("recipient").get("coin")
    self_trx_pubkey = transaction.get("outcoins").get("recipient").get("pubkey")

    for coin in coins_list:
        if coin == self_trx_coin and sender_pub_key == self_trx_pubkey:
            return 1
    return 0


def check_mempool_transaction_coins(coins:list, sender_pub_key:str) -> None:
    """
    this function checks to see if for transaction coins that may exist in ledger
    """

    ledger = pypayd.deamon_node.mempool
    for trx in ledger:
        check_incoins(
            transaction=trx,
            coins_list=coins,
            checks_ledger=True
        )


def validate_coin(coins:list, sender_pub_key:str, validating_block_transactions: bool = False) -> bool:
    """
    to solve double spending problem the only requirement is to check imcoins list
    so in this function we are ignoring outcoins
    """
    if not validating_block_transactions:
        check_mempool_transaction_coins(coins, sender_pub_key)

    last_block_index = LAST_BLOCK_INDEX

    if last_block_index <= 0:
        return

    validated_coins_count = 0

    while last_block_index > 0:
        block = blocks[last_block_index - 1] #subtract 1 because list index starts from 0 but block indexes start from 1

        print(f"NUMBER OF TRANSACTIONS IN BLOCK WITH INDEX {last_block_index} IS : {block.get('trxs')}")
        for trx in block.get("trxs"):
            trx_status = trx.get("metadata").get("status")
            print('CHECKING COINS USING BLOCK: ', last_block_index)
            if trx_status == TRX_TYPES.trx:
                check_incoins(trx, coins, last_block_index)
                validated_coins_count += check_outcoins(trx, coins, sender_pub_key)

            elif trx_status == TRX_TYPES.selftrx:
                validated_coins_count += check_selftrx_outcoins(trx, coins, sender_pub_key)

            elif trx_status == TRX_TYPES.trxfee:
                check_trxfee_incoins()
                validated_coins_count += check_trxfee_outcoins(trx, coins, sender_pub_key)

        last_block_index -= 1