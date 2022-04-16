from random import choice, random
import time
import Exceptions


ALPHANUMERIC_CHOICES = "abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPRSTUVWXYZ0123456789" # "Q" cannot be used in coin seed since its a seperation chatacter
SIMILAR_CHARACTERS = "O01l"
COIN_SIZE_48 = 48

class COIN:

    def __init__(self , seed_size:int = 32) -> None:
        self.coin_seed = self.create_seed(seed_size)
        self.coin = ""
        self.is_generated = False

    
    def generate_coin(self, amount:float = 1.0) -> None:
        if self.is_generated == True:
            raise Exceptions.CoinException("coin is already generated use .get_coin to get coin")

        time_stamp = str(time.time())
        amount = str(amount)
    
        coin = time_stamp + "Q" + self.coin_seed + "Q" + amount
        self.coin = coin
        self.is_generated = True
    

    def get_coin(self):
        if self.is_generated == False:
            raise Exceptions.CoinException("coin is not generated")
        
        return self.coin


    @classmethod
    def create_seed(cls, seed_size: int = 32) -> str:
        """
        this method creates a random string using 'ALPHANUMERIC_CHOICES' and avoids using  
        characters if they are duplicates in 'SIMILAR_CHARACTERS'
        """
        
        seed = ""
        for i in range(seed_size):
            choosen_character = choice(ALPHANUMERIC_CHOICES)

            while choosen_character in seed and choosen_character in SIMILAR_CHARACTERS:
                choosen_character = choice(ALPHANUMERIC_CHOICES)

            seed += choosen_character
        
        return seed 


    def cast_coin(self, coins_list : list, amount:float) -> tuple:
        """
            this function returns a tuple containing (coin object, reverse_trx_amount: the amount that should be return to sender)
        """
        tobe_casted_coin_amount = 0.0

        for coin in coins_list:
            coin = coin.split("Q")
            coin_amount = coin[2]
            tobe_casted_coin_amount += float(coin_amount)

        self.generate_coin(amount= amount)
        # if tobe_casted_coin_amount > amount:
        #     self.generate_coin(amount= amount)
        # next line returns the coin and the rest of coins amount, including reverse_amount and trxfee_amount
        return self.get_coin(), tobe_casted_coin_amount - amount # maybe this sould return a tuple consisting two coins instead of one