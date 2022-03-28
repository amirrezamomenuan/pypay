


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
    return


def validate_transaction() -> bool:
    return True