from collections import OrderedDict
from utility.printable import Printable


# Inheritance Printable
class Transaction(Printable):
    """
    A transaction which can be added to a block in the blockchain.

    Attributes:
        :sender: The sender of the coins.
        :recipient: The recipient of the coins.
        :signature: The signature of the transaction.
        :amount: The amount of the coins sent.
    """
    def __init__(self, sender, recipient, signature, amount):
        self.sender = sender                # Public key
        self.recipient = recipient          # Student ID
        self.amount = amount                # Vote
        self.signature = signature          # Signature

    def to_ordered_dict(self):
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])
