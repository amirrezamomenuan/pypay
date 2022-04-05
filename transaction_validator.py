import time
import json
from hashlib import sha256
from collections import OrderedDict
import sys

sys.path.append("..")

import coin_validator
import wallet_cli
import Exceptions


coin_validator = coin_validator

MIN_TRXFEE_AMOUNT = 0.001
MAX_TRX_AMOUNT = 100
MIN_TRX_AMOUNT = 0.1


def get_hashed_signable_data(transaction:dict) -> int:
    # print("this function is performiong...")
    signable_data = OrderedDict()
    signable_data['incoins'] = transaction.get('incoins')
    signable_data['outcoins'] = transaction.get('outcoins')
    signable_data['sender_pubkey'] = transaction.get('sender_pubkey')

    jsonified_signable_data = json.dumps(signable_data, indent=4, sort_keys=True)
    # print("\tfunction: get_hashed_signable_data\n", )
    # print("\tjsonified_signable_data = \n",jsonified_signable_data)
    hexified_data = sha256(jsonified_signable_data.encode()).hexdigest()
    # print("hexified data is : ", hexified_data, "\n\n")
    return int(hexified_data, 16)


def unsign_signature(signature:int, pubkey_as_keypair:str) -> str:
    return wallet_cli.unsign_transaction_signature(signature=signature, pubkey_as_keypair= pubkey_as_keypair)


def trx_timestamp_validator(time_stamp:float) -> None:
    if time.time() < time_stamp:
        raise ValueError("timestamp cannot be in the future")


def trx_status_validator(status:str) -> None:
    if status not in ('trxfee', 'trx', 'selftrx'):
        raise ValueError(f"invalid transaction status : {status}")


def trx_metadata_validator(metadata:dict) -> None:
    trx_timestamp_validator(metadata.get("ts"))
    trx_status_validator(metadata.get("status"))


def trxfee_amount_validator(trxfee_coin: str) -> None:
    """
        this function checks to see if the trxfee is less than minimum trxfee amount or 
        if peer didnot put any trxfee on it

        if transaction fee is greater than 0 and lower than minimum trxfee amount this function wont raise any errors
    """
    trxfee_amount = float(trxfee_coin.split("Q")[2])

    if trxfee_amount == 0:
        return

    elif trxfee_amount < 0:
        raise ValueError("trxfee cannot be negative")

    elif trxfee_amount < MIN_TRXFEE_AMOUNT:
        raise ValueError(f"minimum trxfee per transaction is : {MIN_TRXFEE_AMOUNT}")


def transaction_amount_validator(trx_coin: str) -> None:
    """
        this function checks if the transaction amount is in the proper range
    """
    trx_amount = float(trx_coin.split("Q")[2])

    if trx_amount > MAX_TRX_AMOUNT:
        raise ValueError(f"maximum amount for transaction coin is : {MAX_TRX_AMOUNT}")
    elif trx_amount < MIN_TRX_AMOUNT:
        raise ValueError(f"minimum amount for transaction coin is : {MAX_TRX_AMOUNT}")


def trx_structure_validator(transaction:dict) -> None:
    trx_metadata = transaction.get("metadata")
    trx_incoins = transaction.get("incoins")
    trx_outcoins = transaction.get("outcoins")
    trx_signature = transaction.get("signature")
    trx_pubkey = transaction.get("sender_pubkey")

    if type(trx_metadata) not in (dict, OrderedDict):
        raise ValueError("metadata is not in a valid form")

    elif type(trx_incoins) is not list:
        raise ValueError("incoins is not in a valid form")

    elif type(trx_outcoins) not in (dict, OrderedDict):
        # print(trx_outcoins)
        raise ValueError("outcoins is not in a valid form")

    elif type(trx_signature) is not int:
        # it might be a byte string 
        #in that case it will cause some serious problems
        raise ValueError("signature is not in a valid form")
    
    elif type(trx_pubkey) != str:
        # print(trx_pubkey)
        # print(type(trx_pubkey))
        raise ValueError("sender public key is in an invalid form")


def trx_incoins_list_validator(incoins:list, transaction_status:str) -> None:
    if transaction_status != "selftrx":
        if len(incoins) <= 0:
            raise ValueError("incoins cannot be empty unless its a mining reward transaction")


def trx_signarue_validator(transaction:OrderedDict) -> None:
    """
    this function is supposed to unsign signature useing given public key
    and in the second step it should check if the signed data is valid
    """
    signature = transaction.get("signature")
    pubkey_as_keypair = transaction.get("sender_pubkey")
    hashed_signable_data = get_hashed_signable_data(transaction)
    unsigned_hashed_data = unsign_signature(signature, pubkey_as_keypair)

    if unsigned_hashed_data != hashed_signable_data:
        raise ValueError("invalid signature")
    

def validate_input_trx_coins(transaction:OrderedDict, validating_block_transactions:bool = False) -> None:
    """
    this function has to check if the signed coins actually belong to the address that signed it
    """
    incoins_list = transaction.get("incoins")
    sender_pubkey = transaction.get("sender_pubkey")
    # print(incoins_list)
    # print(sender_pubkey)
    coin_validator.validate_coin(incoins_list, sender_pubkey, validating_block_transactions)


def trxfee_validator(fxg):
    # passing due to import error in transaction generator
    return True


def incoins_validator(incoins):
    # passing due to import error in transaction generator
    pass


def validate_transaction(transaction:OrderedDict, validating_block_transactions:bool = False):
    # print("\n\ttransaction validation started...\n")
    trx_structure_validator(transaction= transaction)
    trx_metadata_validator(transaction['metadata'])
    trxfee_amount_validator(transaction['outcoins']['trxfee']['coin'])
    transaction_amount_validator(transaction['outcoins']['recipient']['coin'])
    trx_signarue_validator(transaction = transaction)
    validate_input_trx_coins(transaction = transaction, validating_block_transactions = validating_block_transactions)
    # print("\n\ttransaction validated successfully...")