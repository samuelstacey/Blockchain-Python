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
def get_user_input():
    userin = input("Input: ")
    return userin


add_value(get_user_input())

#while loop for getting inputs
while True:
    print('Please choose an option')
    print('1. Add transaction')
    print('2. Ouput current transactions')

    selected_option = get_user_input()

    if (selected_option == '1'):
        print("Please enter transaction value")
        add_value(float(get_user_input()), get_last_transaction_amount())
    elif (selected_option == '2'):
        # output the blockchain list to console
        for block in blockchain:
            print(block)
    else:
        print('Please enter a valid option from the list')
    


