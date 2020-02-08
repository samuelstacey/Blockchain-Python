# initialising blockchain list
blockchain = []
open_transactions = []
owner = 'Sam'

# function to add transaction to blockchain


def add_transaction(sender, recipient, amount=1.0):
    """ Add a transaction to a blockchain
    Arguments:
        :sender: The sender of the coins
        :receiver: The receiver of the coins
        :amount: The value of the transaction, default is 1
    """
    transaction = {'sender': sender, 'recipient': recipient, 'amount':amount}
    open_transactions.append()


# return last transaction amount
def get_last_transaction_amount():
    """Returns the last value of the current blockchain without popping"""
    if len(blockchain) > 0:
        return blockchain[-1]
    else:
        return 0


# gets user input
def get_user_input():
    userin = input("Input: ")
    return userin


def get_transaction_input():
    tx_recipient = input('Enter recipient address: ')
    tx_amount = float(input('Enter transaction amount: '))
    return tx_recipient, tx_amount


# output the blockchain list to console
def print_blockchain():
    if len(blockchain) > 0:
        for block in blockchain:
                print(block)
    else:
        print("The blockchain is empty")


def mine_block():
    pass


#Validates the blockchain to ensure that it hasn't been manipulated
def chain_verification():
    block_index = 0
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif (blockchain[block_index][0] != blockchain[block_index - 1]):
            is_valid = False
            break
    return is_valid
    
waiting_for_input = True

#while loop for getting inputs
while waiting_for_input:
    print('Please choose an option')
    print('1: Add transaction')
    print('2: Ouput current transactions')
    print('h: Manipulate the chain')
    print('q: Quit')

    #variable to hold user input
    selected_option = get_user_input()

    #if statement to run based on user input
    if (selected_option == '1'):
        tx_amount = get_transaction_input
        print("Please enter transaction value")
        add_transaction(tx_amount, get_last_transaction_amount())
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
