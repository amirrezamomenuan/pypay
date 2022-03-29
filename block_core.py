# from block_validator import validate_block
import block_validator
validate_block = block_validator.validate_block
import Exceptions


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


def handle_new_block(block:dict, last_block:dict = {}) -> tuple:
    try:
        validate_block(block = block, last_block = last_block)
        return "block added to chain successfully, Congratulations!", 200

    except Exceptions.CoinException:
        return "this block contains invalid coins!", 400

    except Exceptions.DoubleSpendError:
        return "this block cointains a coin that is already consumed", 400

    except Exceptions.InvalidBlock:
        return "this is an invalid block check structure or metadata and validate transactions", 400

    else:
        return "this block failed to validate due to an unexpected error", 400
