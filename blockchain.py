import functools 
from utility.hash_util import hash_block #My library for hashing 
import json
from block import Block
from transaction import Transaction
from utility.verification import Verification

# reward for mining a single block given to the miner
MINING_REWARD = 10

class Blockchain:
    def __init__(self, hosting_node_id):
        #first block of the chain stored as an object
        genesis_block =  Block(0, '', [], 100, 0)
        #Initialising empty blockchain list
        self.__chain = [genesis_block]
        #list of open transactions  
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

    def get_chain(self):
        return self.__chain[:]

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                    file_content = f.readlines()
                    blockchain = json.loads(file_content[0][:-1])
                    updated_blockchain = []
                    for block in blockchain:
                        converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]
                        updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                        updated_blockchain.append(updated_block)
                    self.__chain = updated_blockchain
                    open_transactions = json.loads(file_content[1])
                    updated_transactions = []
                    for tx in open_transactions:
                        updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                        updated_transactions.append(updated_transaction)
                    self.__open_transactions = updated_transactions
        except (FileNotFoundError, IndexError):
            print("File created")
                  

    def save_data(self):
        try:
            with open('blockchain.txt', mode='w') as f:
                    saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                    f.write(json.dumps(saveable_chain))
                    f.write('\n')
                    saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                    f.write(json.dumps(saveable_tx))
        except IOError:
            print("Saving failed.")


    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_POW(self.__open_transactions, last_hash, proof):
            proof +=1
        return proof


    # get the balance of a user based on transaction history
    def get_balance(self):
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions
                    if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount
                        for tx in self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
        tx_receiver = [[tx.amount for tx in block.transactions
                        if tx.recipient == participant] for block in self.__chain]
        amount_received = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_receiver, 0)
        return amount_received - amount_sent

    # return last transaction amount 
    def get_last_transaction_amount(self):
        """Returns the last value of the current blockchain without popping"""
        if len(self.__chain) > 0:
            return self.__chain[-1]
        else:
            return 0

    # function to add transaction to blockchain
    def add_transaction(self, recipient, sender, amount=1.0):
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
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False
        

    # mine block and produce mining rewars as well as verifying transactions
    def mine_block(self):
        last_block = self.__chain[-1]
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        #transaction for mining the block added when block is mined
        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }
        reward_transaction = Transaction('MINING', self.hosting_node, MINING_REWARD)
        #copied so that the mining transaction only completes if the block is mined successfully
        copied_transactions = self.__open_transactions[:]
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
        #block added to chain therefore mined
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return True
