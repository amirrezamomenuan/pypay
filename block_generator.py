import time
import json
from random import shuffle
from hashlib import sha256
from collections import OrderedDict
import requests

import block_core
import Exceptions
import pypayd

EMPTY_STR_HASH = "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
TRX_LIST_LIMIT = 10


class BLOCK:
    def __init__(self, last_block_index:int, lastblock_hash:str):
        self.index = last_block_index + 1
        self.lastblock_hash = lastblock_hash
        self.trxs = []
        self.can_have_trxfee_trx = False
    
    def _generate_metadata(self) -> None:
        setattr(self, 'metadata', OrderedDict())
        self.metadata['ts'] = time.time()
        self.metadata['nonce'] = 0
        self.metadata['index'] = self.index
        self.metadata['lastblock_hash'] = self.lastblock_hash

    def __increment_nonce(self) -> None:
        self.metadata['nonce'] += 1
    

    def __update_ts(self) -> None:
        self.metadata['ts'] = time.time()
    

    def __add_trx_to_trxs(self, trx:OrderedDict) -> None:
        self.trxs.append(trx)


    def _generate_trxs_list(self, transactions_list:list) -> None:
        trx_number = 0
        for trx in transactions_list:
            self.__add_trx_to_trxs(trx)

            if trx['metadata']['status'] != 'selftrx' or trx['metadata']['status'] != 'trxfee':
                trx_number += 1
            if trx_number >= TRX_LIST_LIMIT:
                break
        
        # add another function here that adds selftrx and trxfee trx to transactions_list

    def __stirngify_hashable_data(self) -> str:
        stringified_data = json.dumps(self.hashable_data, sort_keys= True)
        return stringified_data


    def __cast_hashable_block(self) -> str:
        if hasattr(self, 'hashable_data'):
            return self.__stirngify_hashable_data()

        hashable_data = OrderedDict()
        hashable_data['metadata'] = self.metadata
        hashable_data['trxs'] = self.trxs
        setattr(self, 'hashable_data', hashable_data)

        return self.__stirngify_hashable_data()
    

    def __update_hashable_block(self):
        self.__increment_nonce()
        self.__update_ts()


    def __hash_block(self) -> str:
        stringified_data = self.__cast_hashable_block()
        hashed_data = sha256(stringified_data.encode())
        human_readable_hashed_data = hashed_data.hexdigest()
        setattr(self, 'hashed_data_result', human_readable_hashed_data)
        return human_readable_hashed_data


    def __check_hash_is_acceptable(self, hashed_string:str) -> bool:
        return hashed_string[:4] == '0000'


    def __add_mining_reward(self):
        # check the trxfee protocol later
        self_trx = block_core.generate_selftrx_transaction()
        trxfee = block_core.generate_trxfee_transaction()

        self.__add_trx_to_trxs(self_trx)
        if trxfee is not None:
            self.__add_trx_to_trxs(trxfee)
    

    def __check_self_trx_existance(self):
        if len(self.trxs) == 0:
            raise Exception("can not check an empty list")

        for trx in self.trxs:
            try:
                if trx['metadata']['status'] == "selftrx":
                    return True
            except:
                raise Exceptions.SelfTrxDoesNotExist("invalid trx structure in block_generator >> __check_self_trx_existence")
        raise Exceptions.SelfTrxDoesNotExist("self transaction is not included in trxs")
    

    def __check_trxfee_trx_existance(self):
        if self.can_have_trxfee_trx:
            for trx in self.trxs:
                try:
                    if trx['metadata']['status'] == "trxfee":
                        return True
                except:
                    raise Exceptions.TrxfeeTrxDoesNotExist("invalid trx structure in block_generator >> __check_trxfee_trx_existance")

            error_message = """this set of transactions includes transaction(s) 
            that have considerable trxfees that are not contained in transactions list"""
            raise Exceptions.TrxfeeTrxDoesNotExist(error_message)


    def _mine_block(self, transactions_list:list, max_nonce_limit:int = 1000000000) -> dict:

        self._generate_metadata()
        self._generate_trxs_list(transactions_list= transactions_list)
        self.__check_self_trx_existance()
        self.__check_trxfee_trx_existance()
        # self.__add_mining_reward()

        while  self.metadata['nonce'] < max_nonce_limit:
            if self.__check_hash_is_acceptable(self.__hash_block()):
                print(self.hashable_data)
                return self.hashable_data
            self.__update_hashable_block()
        return None


    def _shuffle_trxs(self):
        shuffle(self.trxs)


def mine(transactions_list:list, lastblock_index:int = 0, lastblock_hash:str = EMPTY_STR_HASH):
    block = BLOCK(last_block_index = lastblock_index, lastblock_hash= lastblock_hash)

    while True:
        if block._mine_block(transactions_list= transactions_list) is not None:
            # passing all next lines to block core
            # block_core.add_block_to_chain(block= block.hashable_data) # commented to prevent adding block before sending to other nodes
            print("data hash when mining is: ", block.hashed_data_result)
            pypayd.deamon_node.remove_transactions_list(block.hashable_data.get("trxs"))# delete from here and add after validated
            block_core.send_newly_mined_block_to_all_neighbour_nodes(block= block.hashable_data) 
            return

        else:
            block._shuffle_trxs()