

class chain:
    def __init__(self, initial_chain: list = []):
        self.__chain:list = initial_chain
    
    
    def update_chain(self, point:int, chain_difference:list):
        self.__chain = self.__chain[:point] + chain_difference
    

    def append_new_block(self, block):
        self.__chain.append(block)
    

    def get_full_chain(self):
        return self.__chain[:]
    
    
    @property
    def last_block(self):
        if len(self.__chain) > 0:
            return self.__chain[-1]
        else:
            return "genesis block"
    
    @property
    def last_block_index(self) -> int:
        if self.last_block != "genesis block":
            return self.last_block.get("metadata").get('last_block_index')
        
        else:
            return -1