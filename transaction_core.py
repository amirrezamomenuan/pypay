import transaction_generator
import transaction_validator
import Exceptions
import pypayd

def add_transaction_to_mempool(transaction):
    # import pypayd
    pypayd.deamon_node.add_transaction_to_mempool(transaction)

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


        # transaction = transaction_core.create_transaction(
        #     pubkey = f"{self.__e},{self.__n}",
        #     recipient_pubkey = recipient_pubkey, 
        #     incoins = incoins,
        #     amount = amount,
        #     trxfee_amount = trxfee_amount,
        # )


def validate_transaction(transaction, is_validating_block: bool = False) -> bool:
    try:
        # turn dict to ordereddict
        # print("\t\t here we are in validate_transaction in transaction_core")
        transaction_validator.validate_transaction(transaction=transaction, validating_block_transactions=is_validating_block)
        print("executed in area 100")
        if not is_validating_block:
            add_transaction_to_mempool(transaction)
        print("executed in area 101")
        # print("transaction validated and added to mempool")
        return "transaction validated and added to mempool", 200
    except Exceptions.InvalidBlock:
        # print("this block is invalid")
        return "this block is invalid", 400
    except Exceptions.CoinException:
        # print("there is something wrong with the coins")
        return "there is something wrong with the coins", 400
    except Exceptions.DoubleSpendError:
        # print("coin(s) in incoins are spent before make sure to update incoins file")
        return "coin(s) in incoins are spent before make sure to update incoins file", 400
    except Exceptions.CoinDoesNotBelongToSenderError as e:
        return f"Coin error : {e}", 400
    except ValueError as ve:
        # print(f"you gave an invalid value {ve}")
        return f"you gave an invalid value {ve}", 400
    except Exception as e:
        print("this is an error", e)
        raise Exception(f"{e}")


    