import threading
import requests

import block_validator,block_generator
import Exceptions
import pypayd
import wallet_cli
import transaction_core

def generate_selftrx_transaction():
    self_trx_mining_reward = wallet_cli.wallet().create_self_trx()
    pypayd.deamon_node.add_transaction_to_mempool(self_trx_mining_reward, start_minig=False)


def generate_trxfee_transaction():
    trxfee_mining_trx = wallet_cli.wallet().create_trxfee_trx(pypayd.deamon_node.mempool)
    pypayd.deamon_node.add_transaction_to_mempool(trxfee_mining_trx, start_minig=False)


def create_block_minable_data() -> dict:
    last_block_metadata = pypayd.deamon_node.get_last_block().get("metadata")
    print("last block metadata is: ", last_block_metadata)
    if last_block_metadata is not None:
        last_block_index = last_block_metadata.get('index')
        #the next line was a huge problem and was made by lack of consentration
        #it was using the last blocks lastblock_hash instead of 
        # generating it by hashing last block

        # last_block_hash = last_block_metadata.get('lastblock_hash') # no you fucking idiot
        last_block_hash = pypayd.deamon_node.get_last_block_hash() # going to find or write a fumction or method
    else:
        last_block_hash = "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
        last_block_index = 0
        
    data = {
        'transactions_list':pypayd.deamon_node.mempool,
        'lastblock_index':last_block_index,
        'lastblock_hash':last_block_hash
    }
    return data


def mine_block():
    generate_trxfee_transaction()
    generate_selftrx_transaction()
    minable_block_data = create_block_minable_data()
    mine_thread = threading.Thread(target=block_generator.mine, kwargs=minable_block_data)
    mine_thread.start()


def send_newly_mined_block_to_all_neighbour_nodes(block:dict):
    print("HERE TRYING TO SEND BLOCK TO RELATIVE NODES")
    for node in pypayd.deamon_node.relative_nodes:
        url ='http://' + node + "/new-block"
        try:
            requests.post(url=url, json= block)
        except:
            pass


def add_block_to_chain(block):
    pypayd.deamon_node.add_block_to_chain(block)


def handle_new_block(block:dict, last_block:dict = {}) -> tuple:
    try:
        block_validator.validate_block(block = block, last_block = last_block)
        add_block_to_chain(block= block)
        pypayd.deamon_node.remove_transactions_list(transactions_list= block.get('trxs'))
        print("block validated and added to chain successfully")
        return "block validated and added to chain successfully", 200
    except Exceptions.CoinException:
        print("this block contains invalid coins!", 400)
        return "this block contains invalid coins!", 400
    except Exceptions.DoubleSpendError:
        print("this block cointains a coin that is already consumed")
        return "this block cointains a coin that is already consumed", 400
    except Exceptions.InvalidBlock as be:
        print(f" invalid block: {be}")
        return f" invalid block: {be}", 400
    except Exceptions.InvalidTransaction as te:
        print(f"invalid transaction(s) : {te}")
        return f"invalid transaction(s) : {te}", 400
    except:
        print(f"this block failed to validate due to an unexpected error")
        return f"this block failed to validate due to an unexpected error", 400