blockchain = []

def add_value(transaction_amount, last_transaction = 0):
    blockchain.append([last_transaction,transaction_amount])


def get_last_transaction_amount():
    return blockchain[-1]

add_value(5.6)
add_value(3.2, get_last_transaction_amount())
add_value(8.4, get_last_transaction_amount())

print(blockchain)