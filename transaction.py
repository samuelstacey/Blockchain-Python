import collections
from utility.printable import Printable

#holds transactions as an object until they are added to the chain
class Transaction(Printable):
    def __init__(self, sender, recipient, signature,  amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    def to_ordered_dict(self):
        return collections.OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])