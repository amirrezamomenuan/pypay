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

        self.has_transaction_fee = trxfee_validator(trxfee_amount)
        transaction_amount_validator(amount)
        incoins_validator(incoins)


    def validate_incoins(self) -> None:
        coin_validator.validate_coin(coins= self.incoins, sender_pub_key= self.pubkey)
    
    
    @staticmethod
    def __cast_coin(self, amount:float, pubkey:str, incoin_list:list = []) -> OrderedDict:
        if len(incoin_list) > 0:
            coin = coin_generator.COIN(coin_generator.COIN_SIZE_48)
            cast_data = coin.cast_coin(incoin_list, amount)
            coin = cast_data[0]
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
        
        if self.has_transaction_fee:
            self.outcoins['trxfee'] = self.__cast_coin(self, amount=self.trxfee_amount, pubkey="miner")
        

    def __construct_signable_hashed_data(self) -> str:
        signable_data = OrderedDict()
        signable_data['incoins'] = self.incoins
        signable_data['outcoins'] = self.outcoins
        signable_data['pubkey'] = self.pubkey

        jsonified_signable_data = json.dumps(signable_data)
        # print(jsonified_signable_data)
        # setattr(self, "has_signable_data", True)
        return sha256(jsonified_signable_data.encode()).hexdigest()


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
        transaction['signature'] = self.siganture
        transaction['sender_pubkey'] = self.pubkey

        setattr(self, "forged_transaction", transaction)


    def get_transaction(self):
        if not hasattr(self, "forged_transaction"):
            raise ValueError("TRANSACTION object has no attrubute forged_transaction, please make sure to call cast_transaction method")
        
        return self.forged_transaction


# trx = TRANSACTION("rezaishere1378", "rezaisthere13780", incoins=['16551025.0215QthisisacoinQ15.000'], amount=15, trxfee_amount=0)
# trx.cast_coin(amount = 14.5, pubkey = trx.pubkey, incoin_list= trx.incoins)
# trx.__cast_outcoins()
# print(trx.construct_signable_data())