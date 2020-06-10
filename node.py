from flask import Flask, jsonify, request, send_from_directory #jsonify just like json dumps really, request gets data sent with POST request
from flask_cors import CORS

from wallet import Wallet
from blockchain import Blockchain


app = Flask(__name__)
wallet = Wallet() #no real public key yet
blockchain = Blockchain(wallet.public_key)
CORS(app) #To open to other clients not on the same node#


#Tells flask if domain/ with get method return this 
@app.route('/', methods=['GET']) #Just an endpoint for external http requests 
def get_node_ui():
    return send_from_directory('UI', 'node.html')

@app.route('/network', methods=['GET']) 
def get_network_ui():
    return send_from_directory('UI', 'network.html')


@app.route('/wallet', methods = ['POST'])
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)  #recreate blockchain with new keys
        response = { #Decides return message
            'public_key' : wallet.public_key, 
            'private_key' : wallet.private_key,
            'balance': blockchain.get_balance()
        }
        return jsonify(response), 201
    else: 
        response = { #Decides error message
            'message' : 'Saving the keys failed', 
        }
        return jsonify(response), 500 #CHECK AGAIN


@app.route('/wallet', methods = ['GET'])
def load_keys(): #THIS DOES NOT WORK
    if wallet.load_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)  #recreate blockchain with new keys
        response = { #Decides return message
            'public_key' : wallet.public_key, 
            'private_key' : wallet.private_key,
            'balance': blockchain.get_balance()
        }
        return jsonify(response), 201 #success response code
    else: 
        response = { #Decides error message
            'message' : 'Loading the keys failed', 
        }
        return jsonify(response), 500 #CHECK AGAIN


@app.route('/transactions', methods=['GET'])
def get_open_transactions():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return jsonify(dict_transactions), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_to_return = blockchain.get_chain()
    dict_chain = [block.__dict__.copy() for block in chain_to_return] #to make the block object serialiseable within the chain
    for dict_block in dict_chain:
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']] #to make the transaction object serialiseable within block
    return jsonify(dict_chain), 200


@app.route('/balance', methods=['GET'])
def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            'message': 'Retrieving balance Succeeded',
            'balance': balance
        } 
        return jsonify(response), 200
    else:
        response = {
            'message': 'Retrieving balance failed',
            'wallet_set_up': wallet.public_key !=None
        }
        return jsonify(response), 500


@app.route('/transaction', methods=['POST'])
def add_transaction():
    if wallet.public_key == None:
        response = { 
            'message' : 'No wallet setup'
        }
        return jsonify(response), 400
    inputs = request.get_json()
    if not inputs:
        response = {
            'message' : 'No data found'
        }
        return jsonify(response), 400
    required_fields = ['recipient', 'amount']
    if not all(field in inputs for field in required_fields):
        response = {
            'message' : 'Required data is missing'
        }
        return jsonify(response), 400
    recipient = inputs['recipient']
    amount = inputs['amount']
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(recipient, wallet.public_key, signature, amount)
    if success:
        response = {
            'message' : 'Successfully added transaction',
            'transaction': {
                'sender': wallet.public_key,
                'recipient': recipient,
                'amount': amount,
                'signature': signature
            },
            'balance': blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = {
            'message' : 'Creating a transaction failed'
        }
        return jsonify(response), 500


@app.route('/mine', methods=['POST'])
def mine():
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']] #to allow jsonify serialisation
        response = { #Decides return message
            'message' : 'Block added successfully', 
            'block' : dict_block,
            'balance' : blockchain.get_balance()
        }
        return jsonify(response), 201
    else:
        response = { #Decides error message
            'message' : 'Adding a block failed.', 
            'wallet_set_up' : wallet.public_key != None
        }
        return jsonify(response), 500 #CHECK THIS ERROR CODE, NOT SURE


@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data attached'
        }
        return jsonify(response), 400
    if 'node' not in values:
        response = {
            'message': 'No node data attached'
        }
        return jsonify(response), 400
    node = values['node']
    blockchain.add_peer_node(node)
    response = {
        'message': 'Node added successfully',
        'all_nodes': blockchain.get_peer_nodes()
    }    
    return jsonify(response), 201
    
@app.route('/node/<node_ip>', methods=['DELETE'])
def remove_node(node_ip):
    if node_ip == '' or node_ip == None:
        response = {
            'message': 'No node found'
        }
        return jsonify(response), 400
    blockchain.remove_peer_node(node_ip)
    response = {
        'message': 'Node removed',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 201


@app.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = blockchain.get_peer_nodes()
    response = {
        'all_nodes': nodes
    }
    return jsonify(response), 200


if __name__ == '__main__': #Only if directly started the file
    app.run(host='0.0.0.0', port=5000)