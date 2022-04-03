# from block_validator import validate_block
import sys

import block_validator,block_generator
import Exceptions
import pypayd


def fetch_trxd_from_mempool():
    pass

def create_block():
    pass

def mine_block():
    pass


def generate_selftrx_transaction():
    pass

def generate_trxfee_transaction(transaction_list:list):
    pass


def add_block_to_chain(block):
    pypayd.deamon_node.add_block_to_chain(block)


def handle_new_block(block:dict, last_block:dict = {}) -> tuple:
    try:
        last_block = pypayd.deamon_node.get_last_block()
        block_validator.validate_block(block = block, last_block = last_block)
        add_block_to_chain(block= block)
        return "block validated and added to chain successfully", 200

    except Exceptions.CoinException:
        return "this block contains invalid coins!", 400
    except Exceptions.DoubleSpendError:
        return "this block cointains a coin that is already consumed", 400
    except Exceptions.InvalidBlock as be:
        return f" invalid block: {be}", 400
    except Exceptions.InvalidTransaction as te:
        return f"invalid transaction(s) : {te}", 400
    except:
        return f"this block failed to validate due to an unexpected error", 400
