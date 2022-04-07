import json
from hashlib import sha256


import network
import chain
import mempool

import block_core

chain = chain.chain()
mempool = mempool.mempool()

MIN_TRXS_TO_MINE_BLOCK:int = 2
INITIAL_NODES_LIST:list = [
    "127.0.0.1:8000",
    "127.0.0.1:9000",
]


class BlockChain:
    def __init__(self, chain, mempool, relative_nodes):
        self.__chain = chain
        self.__mempool = mempool
        self.__relative_nodes = relative_nodes
    

    @property
    def full_chain(self):
        return self.__chain.get_full_chain()

    @property
    def mempool(self):
        return self.__mempool.get_all_transactions()
    
    @property
    def relative_nodes(self):
        return self.__relative_nodes
    

    def __start_mining(self):
        block_core.mine_block()
        

    def get_last_block(self):
        try:
            return self.__chain.get_full_chain()[-1]
        except:
            return {}
        

    def get_last_block_hash(self) -> str:
        try:
            last_block = self.get_last_block()
            last_block_hash = sha256(json.dumps(last_block).encode()).hexdigest()
            return last_block_hash
        except:
            return "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a" # it is hard coded and very bad

    
    def add_transaction_to_mempool(self, transaction:dict, start_minig:bool = True) -> None:
        self.__mempool.add_transaction(transaction = transaction)
        if self.__mempool.number_of_transactions >= MIN_TRXS_TO_MINE_BLOCK and start_minig is True:
            self.__start_mining()
            
    
    def add_block_to_chain(self, block):
        self.__chain.append_new_block(block)
        print(self.__chain.get_full_chain())
    

    def remove_transactions_list(self,transactions_list: list) -> None:
        self.__mempool.remove_transactions_list(to_be_removed_transactions = transactions_list)














deamon_node = BlockChain(
    chain = chain,
    mempool= mempool,
    relative_nodes= INITIAL_NODES_LIST
    )


if __name__ == "__main__":
    """
    the port should be 80 but since the test is running on a local machine
    i am using ports but it is not required in production mode
    """
    port_number = input("enter your port except(8000, 9000): ")
    network.app.run(port=int(port_number), debug=False)