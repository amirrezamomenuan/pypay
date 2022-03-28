class mempool:
    def __init__(self, initial_transactions = []):
        self.__ledger = initial_transactions
    

    def add_transactions(self, transaction):
        self.__ledger.append(transaction)
    

    def get_all_transactions(self):
        return self.__ledger[:]
    

    def reset_ledger(self):
        self.__ledger.clear()
    

    def remove_transaction(self, transaction):
        try:
            self.__ledger.remove(transaction)
            return "transaction deleted successfully"
        except ValueError:
            return "transaction not in this mempool"
    

    def remove_transactions_list(self, to_be_removed_transactions: list):
        for trx in to_be_removed_transactions:
            self.remove_transaction(trx)
    

    def get_transactions_list_by_given_key(self,given_key:str = 'trxfee', list_size : int = 10, reverse : bool = False):
        temp_ledger = []
        if given_key == "trxfee":
            for trx in self.__ledger:
                try:
                    temp_ledger.append(trx['outcoins'][given_key]['coin'])
                except:
                    pass
        else:
            temp_ledger = self.__ledger

        temp_ledger = sorted(temp_ledger, key= lambda x: x['outcoins'][given_key]['coin'].split('Q')[2], reverse=reverse)

        try:
            return temp_ledger[:list_size]
        except IndexError:
            remained_data_count = list_size - len(temp_ledger)
            for rtrx in self.__ledger:
                if rtrx not in temp_ledger:
                    temp_ledger.append(rtrx)
                    remained_data_count -= 1

                if remained_data_count == 0:
                    break
            return temp_ledger