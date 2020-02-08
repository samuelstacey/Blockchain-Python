# initialising blockchain list
blockchain = []

# function to add transaction to blockchain


def add_value(transaction_amount, last_transaction):
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


#Validates the blockchain to ensure that it hasn't been manipulated
def chain_verification():
    block_index = 0
    is_valid = True
    for block in blockchain:
        if block_index == 0:
            block_index += 1
            continue
        elif (block[0] != blockchain[block_index - 1]):
            is_valid = False
    return is_valid
    
waiting_for_input = True

#while loop for getting inputs
while waiting_for_input:
    print('Please choose an option')
    print('1: Add transaction')
    print('2: Ouput current transactions')
    print('h: Manipulate the chain')
    print('q: Quit')

    selected_option = get_user_input()

    if (selected_option == '1'):
        print("Please enter transaction value")
        add_value(float(get_user_input()), get_last_transaction_amount())
    elif (selected_option == '2'):
        print_blockchain() 
    elif (selected_option == 'q'):
        waiting_for_input = False
    elif (selected_option == 'h'):
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    else:
        print('Please enter a valid option from the list')
    if not chain_verification():
        print("Chain not secure!")
        waiting_for_input = False
