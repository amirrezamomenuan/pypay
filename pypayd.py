import threading


from network import app

if __name__ == "__main__":
    app.run(port=8000)


class BlockChain:
    def __init__(self):
        self.__chain = []
        self.__mempool = []
        self.__relative_nodes = []
    

    @property
    def full_chain(self):
        return self.__chain

    @property
    def mempool(self):
        return self.__mempool
    
    @property
    def relative_nodes(self):
        return self.__relative_nodes
    
    def get_last_block(self):
        try:
            return self.__chain[-1]
        except:
            return {}

deamon_node = BlockChain()