import time
# from time import time
from utility.printable import Printable


# Inheritance Printable
class Block(Printable):
    # Constructor
    # time default: time=time()
    def __init__(self, index, previous_hash, transactions, proof, time=(time.asctime(time.localtime(time.time())))):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time
        self.transactions = transactions
        self.proof = proof
