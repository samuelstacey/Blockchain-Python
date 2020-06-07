from uuid import uuid4 #for a unique node id
from blockchain import Blockchain
from utility.verification import Verification
from wallet import Wallet

class Node:

    def __init__(self):
        # self.wallet = str(uuid4())
        self.wallet = Wallet() #used for debugging before wallets are implemented
        self.blockchain = None


    # gets user input
    def get_user_input(self):
        userin = input("Input: ")
        return userin


    # gets transaction details from user input
    def get_transaction_input(self):
        tx_recipient = input('Enter recipient address: ')
        tx_amount = float(input('Enter transaction amount: '))
        #returns a tuple containing transaction details
        return tx_recipient, tx_amount


    # output the blockchain list to console
    def print_blockchain(self):
        if len(self.blockchain.get_chain()) > 0:
            for block in self.blockchain.get_chain():
                print(block)
        else:
            print("The blockchain is empty")


    def listen_for_input(self):
        waiting_for_input = True
        # while loop for getting inputs
        while waiting_for_input:
            print('Please choose an option')
            print('1: Add transaction')
            print('2: Output blockchain')
            print('3: Mine a new block')
            print('4: Check transaction validity')
            print('5: Create Wallet')
            print('6: Load Wallet')
            print('q: Quit')

            # variable to hold user input
            selected_option = self.get_user_input()

            # if statement to run based on user input
            if (selected_option == '1'):
                tx_data = self.get_transaction_input()
                recipient, amount = tx_data
                if self.blockchain.add_transaction(recipient, self.wallet.public_key, amount=amount):
                    print('Transaction added')
                else:
                    print('Transaction failed')
                print(self.blockchain.get_open_transactions())
            elif (selected_option == '2'):
                self.print_blockchain()
            elif (selected_option == '3'):
                if not self.blockchain.mine_block():
                    print("Mining Failed, You need a Wallet")
                
            elif (selected_option == '4'):
                if Verification.verify_transactions(self.blockchain.get_open_transactions(), self.blockchain.get_balance):
                    print('All transactions are valid')
                else:
                    print('There are invalid transactions')
            elif (selected_option == '5'):
                self.wallet.create_keys()
                self.blockchain = Blockchain(self.wallet.public_key) 
            elif (selected_option == '6'):
                pass
            elif (selected_option == 'q'):
                waiting_for_input = False
            else:
                print('Please enter a valid option from the list')
            if not Verification.chain_verification(self.blockchain.get_chain()):
                print("Chain not secure!")
                waiting_for_input = False
            print('Balance of {}: {:6.2f}'.format(self.wallet.public_key, self.blockchain.get_balance()))

node = Node()
node.listen_for_input()