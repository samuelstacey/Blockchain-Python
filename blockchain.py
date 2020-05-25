import functools 
from hash_util import hash_block, hash_string_256 #My library for hashing 
import json
from block import Block
from transaction import Transaction

# reward for mining a single block given to the miner
MINING_REWARD = 10

owner = 'Sam'
#definition of the blockchain list of blocks
blockchain = []
#list of open transactions  
open_transactions = []

#participants in transactions on the blockchain
participants = {'Sam'}


def load_data():
    global blockchain
    global open_transactions
    try:
        with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                blockchain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                open_transactions = updated_transactions
    except (FileNotFoundError, IndexError):
        print("File not found")
        #first block of the chain stored as an object
        genesis_block =  Block(0, '', [], 100, 0)
        #definition of the blockchain list of blocks
        blockchain = [genesis_block]
        #list of open transactions  
        open_transactions = []
                    

load_data()


def save_data():
    try:
        with open('blockchain.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in blockchain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in open_transactions]
                f.write(json.dumps(saveable_tx))
    except IOError:
        print("Saving failed.")


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
    #transaction = {'sender': sender, 'recipient': recipient, 'amount': amount}
    transaction = Transaction(sender, recipient, amount)
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        save_data()
        return True
    return False


# function to verify whether transaction can be completed based on the sender's balance
def verify_transaction(transaction):
    sender_balance = get_balance(transaction.sender)
    return sender_balance >= transaction.amount


# return last transaction amount 
#NOT WORKING FOR CURRENT IMPLEMENTATION
def get_last_transaction_amount():
    """Returns the last value of the current blockchain without popping"""
    if len(blockchain) > 0:
        return blockchain[-1]
    else:
        return 0


#Check whether a hash is valid, nonce is number only used once
def valid_POW(transactions, last_hash, nonce):
    guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(nonce)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_POW(open_transactions, last_hash, proof):
        proof +=1
    return proof


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
    proof = proof_of_work()
    #transaction for mining the block added when block is mined
    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    #copied so that the mining transaction only completes if the block is mined successfully
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    #block added to chain therefore mined
    blockchain.append(block)
    return True


# get the balance of a user based on transaction history
def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions
                  if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount
                      for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    tx_receiver = [[tx.amount for tx in block.transactions
                    if tx.recipient == participant] for block in blockchain]
    amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_receiver, 0)
    return amount_received - amount_sent


# Validates the blockchain to ensure that it hasn't been manipulated
def chain_verification():
    #enumerate() returns a tuple with indexes and data from blockchain list
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block.previous_hash != hash_block(blockchain[index-1]):
            return False
        if not valid_POW(block.transactions[:-1], block.previous_hash, block.proof): 
            print('Proof of work is invalid')
            return False
    return True


def verify_transactions():
    #Verifies all open transactions
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
            save_data()
    elif (selected_option == '4'):
        print(participants)
    elif (selected_option == '5'):
        if verify_transactions:
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif (selected_option == 'q'):
        waiting_for_input = False
    else:
        print('Please enter a valid option from the list')
    if not chain_verification():
        print("Chain not secure!")
        waiting_for_input = False
    print('Balance of {}: {:6.2f}'.format('Sam', get_balance('Sam')))
