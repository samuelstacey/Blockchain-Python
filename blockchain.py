blockchain = []

def add_value(transaction_amount, last_transaction = [0]):
    blockchain.append([last_transaction,transaction_amount])


def get_last_transaction_amount():
    return blockchain[-1]


tx_amount = float(input("Please enter a transaction amount: "))
add_value(tx_amount)

tx_amount = float(input("Please enter a transaction amount: "))
add_value(tx_amount, get_last_transaction_amount())

tx_amount = float(input("Please enter a transaction amount: "))
add_value(tx_amount, get_last_transaction_amount())

print(blockchain)
