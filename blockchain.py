# initialising blockchain list
blockchain = []

# function to add transaction to blockchain


def add_value(transaction_amount, last_transaction=[0]):
    """ Add a transaction to a blockchain
    Arguments:
        :transaction_amount: The amount of the transaction to be added
        :last_transaction: The value of the previous transaction
    """
    blockchain.append([last_transaction, transaction_amount])


# return last transaction amount
def get_last_transaction_amount():
    """Returns the last value of the current blockchain without popping"""
    return blockchain[-1]


# gets user input for the transaction amount
def get_tx_input():
    tx_amount = float(input("Please enter a transaction amount: "))
    return tx_amount


add_value(get_tx_input())

#while loop for getting inputs
while True:
    add_value(get_tx_input(), get_last_transaction_amount())

    # output the blockchain list to console
    for block in blockchain:
        print(block)
