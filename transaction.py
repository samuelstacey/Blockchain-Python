import collections
from utility.printable import Printable

#holds transactions as an object until they are added to the chain
class Transaction(Printable):
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def to_ordered_dict(self):
        return collections.OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])