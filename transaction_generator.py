import json
import time
from collections import OrderedDict
from hashlib import sha256


import coin_generator, coin_validator


from transaction_validator import (
    trxfee_validator,
    transaction_amount_validator,
    incoins_validator
)


def generate_metadata(trx_type:str = "trx") -> OrderedDict:
    meta_data = OrderedDict()
    meta_data['ts'] = time.time()
    meta_data['status'] = trx_type

    return meta_data


class TRANSACTION:
    def __init__(self, pubkey:str, recipient_pubkey:str, incoins:list, amount:float, trxfee_amount: float= 0) -> None:

        self.incoins = sorted(incoins)
        self.outcoins = OrderedDict()
        self.recipient_pubkey = recipient_pubkey
        self.pubkey = pubkey
        self.trxfee_amount = trxfee_amount
        self.transaction_amount = amount
        self.reverse_transaction_amount = 0.0
        
        # the next three lines may not be required
        self.has_transaction_fee = trxfee_validator(trxfee_amount)
        # transaction_amount_validator(amount)
        incoins_validator(incoins)


    def validate_incoins(self) -> None:
        coin_validator.validate_coin(coins= self.incoins, sender_pub_key= self.pubkey)
    
    
    @staticmethod
    def __cast_coin(self, amount:float, pubkey:str, incoin_list:list = []) -> OrderedDict:
        if len(incoin_list) > 0:
            coin = coin_generator.COIN(coin_generator.COIN_SIZE_48)
            cast_data = coin.cast_coin(incoin_list, amount)
            coin = cast_data[0]
            print(cast_data)
            self.reverse_transaction_amount = cast_data[1] - self.trxfee_amount

        else:
            coin = coin_generator.COIN(coin_generator.COIN_SIZE_48)
            coin.generate_coin(amount=amount)
            coin = coin.get_coin()
        
        final_result = OrderedDict()
        final_result['pubkey'] = pubkey
        final_result['coin'] = coin
        
        return final_result


    def __cast_outcoins(self) -> None:
        self.outcoins['recipient'] = self.__cast_coin(self, amount= self.transaction_amount, pubkey=self.recipient_pubkey, incoin_list=self.incoins)
        
        if self.reverse_transaction_amount > 0:
            self.outcoins['sender'] = self.__cast_coin(self, amount=self.reverse_transaction_amount, pubkey=self.pubkey)
        else:
            self.outcoins['sender'] = {'pubkey': self.pubkey, "coin": None}
        
        if self.has_transaction_fee:
            self.outcoins['trxfee'] = self.__cast_coin(self, amount=self.trxfee_amount, pubkey="miner")
        else:
            self.outcoins['sender'] = {'pubkey': "miner", "coin": None}
        

    def __construct_signable_hashed_data(self) -> int:
        """
        returns a hashed signable data that does not require to be hashed any more
        """
        self.__cast_outcoins() ##############################################################################################################
        signable_data = OrderedDict()
        signable_data['incoins'] = self.incoins
        signable_data['outcoins'] = self.outcoins
        signable_data['sender_pubkey'] = self.pubkey

        jsonified_signable_data = json.dumps(signable_data, indent= 4, sort_keys= True)
        print("jsonified_signable_transaction = ",jsonified_signable_data)
        # setattr(self, "has_signable_data", True)
        data = sha256(jsonified_signable_data.encode()).hexdigest()
        print("signable hashed data in hexdigest form" , data)
        return int(data, 16)


    def get_hashed_signable_data(self):
        return self.__construct_signable_hashed_data()
        

    def set_signature(self, signature):
        setattr(self, "signature", signature)


    def cast_transaction(self, trx_type: str = "selftrx") -> OrderedDict:
        if not hasattr(self,'signature'):
            raise ValueError("transaction has no signature, make sure to call sign before casting transaction")

        transaction = OrderedDict()
        transaction['metadata'] = generate_metadata(trx_type)
        transaction['incoins'] = self.incoins
        transaction['outcoins'] = self.outcoins
        transaction['signature'] = self.signature
        transaction['sender_pubkey'] = self.pubkey

        setattr(self, "forged_transaction", transaction)


    def get_transaction(self):
        if not hasattr(self, "forged_transaction"):
            raise ValueError("TRANSACTION object has no attrubute forged_transaction, please make sure to call cast_transaction method")
        
        return self.forged_transaction