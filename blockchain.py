# initialising blockchain list
genesis_block = {
    'previous_hash': '',
    'index': 0, 
    'transactions': []
}
blockchain = [genesis_block]
open_transactions = []
owner = 'Sam'
participants = {'Sam'}

# function to add transaction to blockchain
def add_transaction(recipient, sender=owner, amount=1.0):
    """ Add a transaction to a blockchain
    Arguments:
        :sender: The sender of the coins
        :receiver: The receiver of the coins
        :amount: The value of the transaction, default is 1
    """
    transaction = {'sender': sender, 'recipient': recipient, 'amount':amount}
    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(recipient)


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
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)

    print(hashed_block)
    block = {
        'previous_hash': hashed_block, 
        'index': len(blockchain), 
        'transactions': open_transactions
    }
    blockchain.append(block)
    return True


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain] 
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_receiver = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_received = 0
    for tx in tx_receiver:
        if len(tx) > 0:
            amount_received += tx[0]
    
    return amount_received - amount_sent



def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


#Validates the blockchain to ensure that it hasn't been manipulated
def chain_verification():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
    return True
    

waiting_for_input = True

#while loop for getting inputs
while waiting_for_input:
    print('Please choose an option')
    print('1: Add transaction')
    print('2: Ouput current transactions')
    print('3: Mine a new block')
    print('4: Output participants')
    print('h: Manipulate the chain')
    print('q: Quit')

    #variable to hold user input
    selected_option = get_user_input()

    #if statement to run based on user input
    if (selected_option == '1'):
        tx_data = get_transaction_input()
        recipient, amount =  tx_data
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif (selected_option == '2'):
        print_blockchain() 
    elif (selected_option == '3'):
        if mine_block():
            open_transactions = []
    elif (selected_option == '4'):
        print(participants)
    elif (selected_option == 'q'):
        waiting_for_input = False
    elif (selected_option == 'h'):
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0, 
                'transactions': [{'sender': 'Mark', 'recipient': 'Sam', 'amount': 100.0}]
            }
    else:
        print('Please enter a valid option from the list')
    if not chain_verification():
        print("Chain not secure!")
        waiting_for_input = False
    print(get_balance('Sam'))