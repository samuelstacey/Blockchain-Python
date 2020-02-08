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
    if len(blockchain) > 0:
        return blockchain[-1]
    else:
        return 0


# gets user input for the transaction amount
def get_user_input():
    userin = input("Input: ")
    return userin


# output the blockchain list to console
def print_blockchain():
    if len(blockchain) > 0:
        for block in blockchain:
                print(block)
    else:
        print("The blockchain is empty")


#while loop for getting inputs
while True:
    print('Please choose an option')
    print('1: Add transaction')
    print('2: Ouput current transactions')
    print('q: Quit')

    selected_option = get_user_input()

    if (selected_option == '1'):
        print("Please enter transaction value")
        add_value(float(get_user_input()), get_last_transaction_amount())
    elif (selected_option == '2'):
        print_blockchain() 
    elif (selected_option == 'q'):
        break
    else:
        print('Please enter a valid option from the list')
