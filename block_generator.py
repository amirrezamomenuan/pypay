import time
import json
from random import shuffle
from hashlib import sha256
from collections import OrderedDict

from block_core import generate_selftrx_transaction, generate_trxfee_transaction

EMPTY_STR_HASH = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
TRX_LIST_LIMIT = 10


class BLOCK:
    def __init__(self, last_block_index:int, lastblock_hash:str):
        self.index = last_block_index + 1
        self.lastblock_hash = lastblock_hash
        self.trxs = []
    
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
            trx_number += 1

            if trx_number >= TRX_LIST_LIMIT:
                break

    def __stirngify_hashable_data(self) -> str:
        stringified_data = json.dumps(self.hashable_data)
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
        return human_readable_hashed_data


    def __check_hash_is_acceptable(self, hashed_string:str) -> bool:
        return hashed_string[:4] == '0000'


    def __add_mining_reward(self):
        # check the trxfee protocol later
        self_trx = generate_selftrx_transaction()
        trxfee = generate_trxfee_transaction(self.trxs)

        self.__add_trx_to_trxs(self_trx)
        if trxfee is not None:
            self.__add_trx_to_trxs(trxfee)
    
    def _mine_block(self, transactions_list:list, max_nonce_limit:int = 1000000000):
        self._generate_metadata()
        self._generate_trxs_list(transactions_list= transactions_list)
        self.__add_mining_reward()

        while  self.metadata['nonce'] < max_nonce_limit:
            if self.__check_hash_is_acceptable(self.__hash_block()):
                return self.hashable_data
            
            self.__update_hashable_block()
        return None


    def _shuffle_trxs(self):
        shuffle(self.trxs)
    

    def __check_self_trx_existance(self):
        if len(self.trxs) == 0:
            raise Exception("can not check an empty list")

        for trx in self.trxs:
            try:
                if trx['metadata']['status'] == "selftrx":
                    return True
            except:
                raise Exception("invalid trx structure in block_generator >> __check_self_trx_existence")
        raise Exception("self transaction is not included in trxs")


def mine(transactions_list:list, last_block_index:int = 0, lastblock_hash:str = EMPTY_STR_HASH):
    block = BLOCK(last_block_index = last_block_index, lastblock_hash= lastblock_hash)
    processed_transactions_list = transactions_list
    while True:
        
        if block._mine_block(transactions_list= transactions_list) is not None:
            print("new block mined")
            return "tell every body"

        else:
            block._shuffle_trxs()




