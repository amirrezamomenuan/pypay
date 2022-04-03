class CoinException(Exception):
    pass

class DoubleSpendError(Exception):
    pass

class InvalidPubKey(Exception):
    pass

class InvalidPrivateKey(Exception):
    pass

class InvalidTransactionStructure(Exception):
    pass

class InvalidTransaction(Exception):
    pass

class InvalidBlock(Exception):
    pass

class SelfTrxDoesNotExist(Exception):
    pass

class TrxfeeTrxDoesNotExist(Exception):
    pass

class InvalidChain(Exception):
    pass