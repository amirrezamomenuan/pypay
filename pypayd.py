import threading


import network
import chain
import mempool
import wallet_cli
import block_generator

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
        self_trx_mining_reward = wallet_cli.wallet().create_self_trx()
        self.add_transaction_to_mempool(self_trx_mining_reward, start_minig=False)

        #create trxfee miner reward trx using wallet-cli and transaction generator
        trxfee_mining_trx = wallet_cli.wallet().create_trxfee_trx(self.__mempool.get_all_transactions())
        self.add_transaction_to_mempool(trxfee_mining_trx, start_minig=False)
        
        # start mining in a new thread and by block generator -> mine()
        last_block_metadata = self.get_last_block().get("metadata")
        if last_block_metadata is not None:
            last_block_index = last_block_metadata.get('index')
            last_block_hash = last_block_metadata.get('lastblock_hash')
        else:
            last_block_hash = "44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"
            last_block_index = 0
        
        
        data = {
            transactions_list:self.__mempool.get_all_transactions(),
            last_block_index:last_block_index,
            last_block_hash:last_block_hash
        }
        mine_thread = threading.Thread(target=block_generator, kwargs=data)
        # if mined a data successfully tell every body using either( mine || deamon node || something else)
        pass


    def get_last_block(self):
        try:
            return self.__chain.get_full_chain()[-1]
        except:
            return {}
    
    def add_transaction_to_mempool(self, transaction:dict, start_minig:bool = True):
        self.__mempool.add_transaction(transaction = transaction)
        if self.__mempool.number_of_transactions >= MIN_TRXS_TO_MINE_BLOCK and start_minig is True:
            self.__start_mining()
            
    
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