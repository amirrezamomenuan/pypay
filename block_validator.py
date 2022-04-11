
import json
from hashlib import sha256
from typing import (
    OrderedDict,
)

from block_generator import TRX_LIST_LIMIT
import transaction_core
import Exceptions

def check_has_metadata(block:OrderedDict):
    if block.get("metadata") is None:
        raise Exceptions.InvalidBlock("block does not have meta data")


def check_time_stamp(block:OrderedDict):
    if block.get("metadata").get('ts') is None:
        raise Exceptions.InvalidBlock("metadata does not have timestamp")


def check_nonce(block:OrderedDict):
    if block.get('metadata').get("nonce") is None:
        raise Exceptions.InvalidBlock("block does not have nonce")
    elif type(block.get('metadata').get("nonce")) != int:
        bad_type = type(block.get('metadata').get("nonce"))
        error_message = f"invalid nonce sent, type : {bad_type} is not acceptable"
        print(error_message)
        raise Exceptions.InvalidBlock(error_message)


def check_index(block:OrderedDict):
    block_index = block.get("metadata").get("index")
    if block_index is None:
        raise Exceptions.InvalidBlock("block does not have index")
    

def check_lastblock_hash(block:OrderedDict):
    lastblock_hash = block.get('metadata').get("lastblock_hash")
    if lastblock_hash is None:
        raise Exceptions.InvalidBlock("lastblock hash does not exist")


def check_has_transactions(block:OrderedDict):
    if block.get("trxs") is None:
        raise Exceptions.InvalidBlock("block does not have transactions")
    elif type(block.get('trxs')) != list:
        raise Exceptions.InvalidBlock(f"block trxs is off type list, {type(block.get('trxs'))} != list ")
    elif len(block.get("trxs")) > TRX_LIST_LIMIT:
        raise Exceptions.InvalidBlock(f"transactions list cannot contain more than {TRX_LIST_LIMIT}")
    elif len(block.get("trxs")) < 1:
        raise Exceptions.InvalidBlock("transactions list most contain at least one trx")


def validate_block_structure(block:OrderedDict) -> bool:
    check_has_metadata(block)
    check_has_transactions(block)
    check_time_stamp(block)
    check_nonce(block)
    check_index(block)
    check_lastblock_hash(block)


def validate_timestamp(block:OrderedDict, last_block_ts:float = 0):
    if block['metadata']['ts'] <= last_block_ts:
        raise Exceptions.InvalidBlock("invalid time stamp , new blocks have been mined")
    

def validate_block_nounce(block: OrderedDict, compared_to_string:str = '0000'):
    stringified_data = json.dumps(block, sort_keys=True)
    hashed_data = sha256(stringified_data.encode()).hexdigest()
    # print("stringified data is: ",stringified_data, '\n\n\n')
    print("hashed data is: ", hashed_data, '\n\n\n')

    # print(hashed_data)
    if hashed_data[:4] != compared_to_string:
        # TODO: add to ban score
        raise Exceptions.InvalidBlock("invalid nonce")


def validate_last_block_hash(block: OrderedDict, last_block_hash:str):
    if last_block_hash != block['metadata']['lastblock_hash']:
        print("last block hash is :" ,last_block_hash)
        print("newblocks lastblock_hash is :", block['metadata']['lastblock_hash'])
        raise Exceptions.InvalidBlock("invalid last block hash")


def validate_index(block:OrderedDict, last_block_index: int = -1):
    block_index = block['metadata']['index']
    if block_index < last_block_index:
        block_index_deffenrence = last_block_index - block_index - 1
        raise Exceptions.InvalidBlock(f'invalid block index: {block_index_deffenrence} blocks have been mined since your last try')
    elif block_index != last_block_index + 1:
        raise Exceptions.InvalidBlock(f'invalid block index: you have mined a block that does not match with last block in chain')


def validate_block_metadata(block:OrderedDict, last_block_ts:float, last_block_index:int, last_block_hash:str):
    validate_timestamp(block, last_block_ts= last_block_ts)

    validate_block_nounce(block) # may cause a problem checkout later on
    
    validate_last_block_hash(block, last_block_hash)
    validate_index(block, last_block_index)


def validate_block_trxs(transactions : list):
    print("\t here we are trying to validate transactions")
    print(len(transactions))
    for trx in transactions:
        # print(type(trx))
        # print(trx)
        trx_validation_result = transaction_core.validate_transaction(transaction=trx, is_validating_block= True)
        if trx_validation_result[1] == 400:
            raise Exceptions.InvalidTransaction(f"{trx_validation_result[0]}")


def validate_block(block:dict, last_block:dict):
    if last_block != {}:
        print("\n\t validating normal block\n")
        last_block_hash = sha256(json.dumps(last_block, sort_keys= True).encode()).hexdigest()
        last_block_index = last_block['metadata']['index']
        last_block_ts = last_block['metadata']['ts']
    
    else:
        print("\n\t validating genesis block\n")
        last_block_hash = '44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a'
        last_block_index = 0
        last_block_ts = 0.0

    validate_block_structure(block = block)
    print("\n\tblock structure validated\n")
    validate_block_metadata(
        block = block,
        last_block_hash= last_block_hash,
        last_block_index=last_block_index,
        last_block_ts=last_block_ts
        )
    print("\n\tblock metadata_validated\n")
    validate_block_trxs(transactions = block['trxs'])
    print("\n\tblock trxs validated\n")
      