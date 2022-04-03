import threading


import network
import chain
import mempool

chain = chain.chain()
mempool = mempool.mempool()

MIN_TRXS_TO_MINE_BLOCK = 5



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
    
    def get_last_block(self):
        try:
            return self.__chain.get_full_chain()[-1]
        except:
            return {}
    
    def add_transaction_to_mempool(self, transaction:dict):
        self.__mempool.add_transaction(transaction = transaction)
        if len(self.__mempool.number_of_transactions) >= MIN_TRXS_TO_MINE_BLOCK:
            print("start mining")
    
    def add_block_to_chain(self, block):
        self.__chain.append_new_block(block)
        print(self.__chain.get_full_chain())


deamon_node = BlockChain(
    chain = chain,
    mempool= mempool,
    relative_nodes= []
    )


if __name__ == "__main__":
    network.app.run(port=8000)