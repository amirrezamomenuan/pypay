import threading


import network
import chain
import mempool

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
        #create selftrx using wallet-cli and transaction generator
        #create trxfee miner reward trx using wallet-cli and transaction generator
        # start mining in a new thread and by block generator -> mine()
        # if mined a data successfully tell every body using either( mine || deamon node || something else)
        pass


    def get_last_block(self):
        try:
            return self.__chain.get_full_chain()[-1]
        except:
            return {}
    
    def add_transaction_to_mempool(self, transaction:dict):
        self.__mempool.add_transaction(transaction = transaction)
        print("number of transactions stacked in mempool is : ", self.__mempool.number_of_transactions)
        if self.__mempool.number_of_transactions >= MIN_TRXS_TO_MINE_BLOCK:
            print("start mining")
    
    def add_block_to_chain(self, block):
        self.__chain.append_new_block(block)
        print(self.__chain.get_full_chain())
    














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