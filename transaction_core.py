import transaction_generator
import transaction_validator
import Exceptions

def create_transaction(pubkey:str, recipient_pubkey:str, incoins:list, amount:float, trxfee_amount: float= 0):
    """
    this function should create a transaction
    and call every required method on transaction object
    then it is supposed to return an unsigned transaction,
    transaction is going to be signed in wallet section 
    and then will add signature to transaction using (.set_signature)
    after casting and finishing the transaction it will be send to network section
    to be sent to other nodes and mempool also.
    """

    transaction = transaction_generator.TRANSACTION(
        pubkey=pubkey,
        recipient_pubkey=recipient_pubkey,
        incoins= incoins,
        amount= amount,
        trxfee_amount= trxfee_amount
    )
    return transaction


def validate_transaction(transaction) -> bool:
    try:
        # turn dict to ordereddict
        transaction_validator.validate_transaction(transaction=transaction)
        return "transaction validated and added to mempool", 200
    
    except Exceptions.InvalidBlock:
        return "this block is invalid", 400
    
    except Exceptions.CoinException:
        return "there is something wrong with the coins", 400
    except Exceptions.DoubleSpendError:
        return "coin(s) in incoins are spent before make sure to update incoins file", 400
    except ValueError as ve:
        return f"you gave an invalid value {ve}", 400
    except:
        return "unexpected error occured", 400
