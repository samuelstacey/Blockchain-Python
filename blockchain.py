import functools
# reward for mining a single block given to the miner
MINING_REWARD = 10
#first block of the chain stored as a dictionary
genesis_block = {
    'previous_hash': '',
    'index': 0,
    'transactions': []
}
#definition of the blockchain list
blockchain = [genesis_block]
#list of open transactions
open_transactions = []
owner = 'Sam'
#participants in transactions on the blockchain
participants = {'Sam'}


# function to add transaction to blockchain
def add_transaction(recipient, sender=owner, amount=1.0):
    """ Add a transaction to a blockchain
    Return: whether transaction was successful
    Arguments:
        :sender: The sender of the coins
        :receiver: The receiver of the coins
        :amount: The value of the transaction, default is 1
    """
    #transaction stored as a dictionary
    transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        return True
    return False


# function to verify whether transaction can be completed based on the sender's balance
def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']


# return last transaction amount 
#NOT WORKING FOR CURRENT IMPLEMENTATION
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


# gets transaction details from user input
def get_transaction_input():
    tx_recipient = input('Enter recipient address: ')
    tx_amount = float(input('Enter transaction amount: '))
    #returns a tuple containing transaction details
    return tx_recipient, tx_amount


# output the blockchain list to console
def print_blockchain():
    if len(blockchain) > 0:
        for block in blockchain:
            print(block)
    else:
        print("The blockchain is empty")


# mine block and produce mining rewars as well as verifying transactions
def mine_block():
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    #transaction for mining the block added when block is mined
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    #copied so that the mining transaction only completes if the block is mined successfully
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions
    }
    #block added to chain therefore mined
    blockchain.append(block)
    return True


# get the balance of a user based on transaction history
def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    #UNDERSTAND THIS
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    tx_receiver = [[tx['amount'] for tx in block['transactions']
                    if tx['recipient'] == participant] for block in blockchain]
    #UNDERSTAND THIS
    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_receiver, 0)
    return amount_received - amount_sent


# return unique hash for a block
def hash_block(block):
    return '-'.join([str(block[key]) for key in block])


# Validates the blockchain to ensure that it hasn't been manipulated
def chain_verification():
    #enumerate() returns a tuple with indexes and data from blockchain list
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index-1]):
            return False
    return True


def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])


waiting_for_input = True

# while loop for getting inputs
while waiting_for_input:
    print('Please choose an option')
    print('1: Add transaction')
    print('2: Ouput current transactions')
    print('3: Mine a new block')
    print('4: Output participants')
    print('5: Check transaction validity')
    print('h: Manipulate the chain')
    print('q: Quit')

    # variable to hold user input
    selected_option = get_user_input()

    # if statement to run based on user input
    if (selected_option == '1'):
        tx_data = get_transaction_input()
        recipient, amount = tx_data
        if add_transaction(recipient, amount=amount):
            print('Transaction added')
        else:
            print('Transaction failed')
        print(open_transactions)
    elif (selected_option == '2'):
        print_blockchain()
    elif (selected_option == '3'):
        if mine_block():
            open_transactions = []
    elif (selected_option == '4'):
        print(participants)
    elif (selected_option == '5'):
        if verify_transactions:
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
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
    print('Balance of {}: {:6.2f}'.format('Sam', get_balance('Sam')))
