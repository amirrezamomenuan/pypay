

class chain:
    def __init__(self, initial_chain: list = []):
        self.__chain:list = initial_chain
    
    
    def update_chain(self, chain:list):
        self.__chain += chain
        print("SELF.CHAIN IS :")
        print(self.__chain)
    

    def append_new_block(self, block):
        self.__chain.append(block)
        print('\n\n\n\t NEW BLOCK APPENDED TO CHAIN\n\n\n')
        print(f'\n\n\n\tCHAIN LENGTH IS {len(self.__chain)}\n\n\n')
    

    def get_full_chain(self):
        return self.__chain[:]
    
    
    @property
    def last_block(self):
        if len(self.__chain) > 0:
            return self.__chain[-1]
        else:
            return "genesis block"
    
    def get_last_block_index(self) -> int:
        return len(self.__chain)