

class Printable:
    def __repr__(self):
        # the self.transaction parameter is converted form def __repr__(self): in transaction.py
        # return 'Index: {}, Previous Hash: {}, Proof: {}, Transactions: {}'.format(self.index, self.previous_hash, self.proof, self.transactions)
        # alternative of code above is the following:
        return str(self.__dict__)