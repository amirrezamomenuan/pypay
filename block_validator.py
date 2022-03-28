
import json
from hashlib import sha256
from typing import (
    OrderedDict,
)

from block_generator import TRX_LIST_LIMIT
from transaction_core import validate_transaction

def check_has_metadata(block:OrderedDict):
    if block.get("metadata") is None:
        raise Exception("block does not have meta data")


def check_time_stamp(block:OrderedDict):
    if block.get("metadata").get('ts') is None:
        raise Exception("metadata does not have timestamp")


def check_nonce(block:OrderedDict):
    if block.get('metadata').get("nonce") is None:
        raise Exception("block does not have nonce")
    elif type(block['nonce']) != int:
        raise Exception(f"invalid nonce sent, type : {type(block['nonce'])} is not acceptable")


def check_index(block:OrderedDict):
    block_index = block.get("metadata").get("index")
    if block_index is None:
        raise Exception("block does not have index")
    

def check_lastblock_hash(block:OrderedDict):
    lastblock_hash = block.get('metadata').get("lastblock_hash")
    if lastblock_hash is None:
        raise Exception("lastblock hash does not exist")


def check_has_transactions(block:OrderedDict):
    if block.get("trxs") is None:
        raise Exception("block does not have transactions")
    elif type(block.get('trxs')) != list:
        raise Exception(f"block trxs is off type list, {type(block.get('trxs'))} != list ")
    elif len(block.get("trxs")) > TRX_LIST_LIMIT:
        raise Exception(f"transactions list cannot contain more than {TRX_LIST_LIMIT}")
    elif len(block.get("trxs")) < 1:
        raise Exception("transactions list most contain at least one trx")


def validate_block_structure(block:OrderedDict) -> bool:
    check_has_metadata(block)
    check_has_transactions(block)
    check_time_stamp(block)
    check_nonce(block)
    check_index(block)
    check_lastblock_hash(block)


def validate_timestamp(block:OrderedDict, last_block_ts:float = 0):
    if block['metadata']['ts'] <= last_block_ts:
        raise Exception("invalid time stamp , new blocks have been mined")
    

def validate_block_nounce(block: OrderedDict, compared_to_string:str = '0000'):
    stringified_data = json.dumps(block)
    hashed_data = sha256(stringified_data.encode()).hexdigest()

    print(hashed_data)
    if hashed_data[:4] != compared_to_string:
        # TODO: add to ban score
        raise Exception("invalid nonce")


def validate_last_block_hash(block: OrderedDict, last_block_hash:str):
    if last_block_hash != block['metadata']['lasblock_hash']:
        raise Exception("hashes dont match")


def validate_index(block:OrderedDict, last_block_index: int = -1):
    block_index = block['metadata']['ts']
    if block_index < last_block_index:
        block_index_deffenrence = last_block_index - block_index - 1
        raise Exception(f'invalid block index: {block_index_deffenrence} blocks have been mined since your last try')


def validate_block_metadata(block:OrderedDict, last_block_ts:float, last_block_index:int, last_block_hash:str):
    validate_timestamp(block, last_block_ts= last_block_ts)
    validate_block_nounce(block)
    validate_last_block_hash(block, last_block_hash)
    validate_index(block, last_block_index)



def validate_block_trxs(transactions : list):
    for trx in transactions:
        validate_transaction(transaction=trx)


def validate_block(block:OrderedDict, last_block):
    if last_block is None:
        print("modify geven data to validate metadata")
    validate_block_structure(block = block)
    validate_block_metadata(block = block)
    validate_block_trxs(transactions = block['trxs'])


# with open('block/structure.json' , 'r') as reader:
#     block = reader.read()

# block = json.loads(block)
# check_block_hash(block)

# print(type(block))

