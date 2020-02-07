blockchain = []

def add_value(transaction_amount, last_transaction = [0]):
    blockchain.append([last_transaction,transaction_amount])


def get_last_transaction_amount():
    return blockchain[-1]


def get_tx_input():
    tx_amount = float(input("Please enter a transaction amount: "))
    return tx_amount

add_value(get_tx_input())
add_value(get_tx_input(), get_last_transaction_amount())
add_value(get_tx_input(), get_last_transaction_amount())

print(blockchain)
