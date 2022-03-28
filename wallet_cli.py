import json
import sys, os

from Crypto.PublicKey import RSA
from hashlib import sha512

import transaction_core


KEYPAIR_FILE_PATH = './wallet'
KEYPAIR_FILE_NAME = 'keypair.json'
COINS = "coins"
BITS_SIZE = 1024
        
class wallet:
    def __init__(self) -> None:
        self.__n = None
        self.__e = None
        self.__d = None
        
        self.__load_wallet_parameters(self.__has_keypair_file(KEYPAIR_FILE_NAME))


    def __has_keypair_file(self, KEYPAIR_FILE_NAME) -> bool:
        return os.path.exists(KEYPAIR_FILE_NAME)
    

    def __load_wallet_parameters(self,has_keypair_file:bool) -> None:
        if has_keypair_file:
            self.__load_parameters_from_file(file_path = KEYPAIR_FILE_PATH, file_name= KEYPAIR_FILE_NAME)
        else:
            self.__generate_key_pair()


    def __generate_key_pair(self, bits_size:int = BITS_SIZE):
        key_pair = RSA.generate(bits=bits_size)
        self.__d = key_pair.d
        self.__n = key_pair.n
        self.__e = key_pair.e

        self.__dump_parameters_to_file(keypair= key_pair , file_path = KEYPAIR_FILE_PATH, file_name= KEYPAIR_FILE_NAME)
    

    def __dump_parameters_to_file(self, keypair, file_path: str, file_name: str):
        dict_data = {"n":keypair.n, "d":keypair.d, "e":keypair.e}
        path_to_json_file = file_path + '/' + file_name
        
        with open(path_to_json_file , "w") as writer:
            json.dump(dict_data, writer)
    

    def __load_parameters_from_file(self, file_path: str, file_name: str):
        path_to_json_file = file_path + '/' + file_name
        
        with open(path_to_json_file , "r") as reader:
            dictified_parameters = json.load(reader)
        
        self.__n = dictified_parameters['n']
        self.__d = dictified_parameters['d']
        self.__e = dictified_parameters['e']
    

    def __hash_transaction(self, hashable_transaction:str) -> int:
        """
        hashes only the important parts of a transaction 
        including incoins
        out coins
        pubkey
        """
        return int.from_bytes(sha512(hashable_transaction.encode()).digest(), byteorder='big')


    def __sign_transaction(self, hashed_trx_data:int) -> str:
        """
        signes hashed_transaction parts
        parts: are described in self.__hash_transaction()
        """
        signature = pow(hashed_trx_data, self.__d, self.__n)
        return hex(signature)
    
    
    def __load_coins_from_jsonfile(self, file_path:str, file_name:str) -> dict: #may need to take it out of class
        # change to read a txt or csv file instead
        path_to_json_file = file_path + '/' + file_name
        
        with open(path_to_json_file , "r") as reader:
            coins_dict = json.load(reader)
        return coins_dict


    def __choose_best_coinset(self, amount:float, trxfee:float = 0) -> list: #may need to take it out of class
        total_amount = amount + trxfee
        coins_dict = self.__load_coins_from_jsonfile(KEYPAIR_FILE_PATH, COINS)
        choosen_coins = []
        max_value = 0
        for k,v in coins_dict.items():
            if v > max_value:
                max_value = v
            if v >= total_amount and v <= max_value:
                choosen_coins.append(k)
            
        if len(choosen_coins) == 0:
            while sum([float(x.split('Q')[2]) for x in choosen_coins]) < total_amount:
                biggest_coin_value = 0
                for k, v in coins_dict.items():
                    if v > biggest_coin_value and v <= total_amount:
                        if k not in choosen_coins:
                            biggest_coin_value = v
                            key = k
                            
                choosen_coins.append(key)

        return choosen_coins                   


    def create_transaction(self, recipient_pubkey:str, amount:float, trxfee_amount:float, trx_type:str = 'trx'): #may need to take it out of class
        incoins = self.__choose_best_coinset(
            amount = amount,
            trxfee = trxfee_amount
            )
        transaction = transaction_core.create_transaction(
            pubkey = f"{self.__e},{self.__n}",
            recipient_pubkey = recipient_pubkey, 
            incoins = incoins,
            amount = amount,
            trxfee_amount = trxfee_amount,
        )

        signable_data = transaction.get_hashed_signable_data()

        signature = self.__sign_transaction(signable_data)
        transaction.set_signature(signature)
        transaction.cast_transaction(trx_type = trx_type)
        return transaction.get_transaction()

    
def unsign_transaction_signature(signature:str, pubkey_as_keypair: str) -> str:
    """
    recieves a transactions hashed signable data and unsign signature
    including:
        incoins,
        outcoins,
        signature

    returns a string wich is equal to unsigned data
    """

    e, n = pubkey_as_keypair.split(",")
    unsign = pow(signature, e, n)
    return hex(unsign)