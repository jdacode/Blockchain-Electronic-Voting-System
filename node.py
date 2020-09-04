"""
send_from_directory = send back a file upon request, in this case HTML file
jsonify = convert json library
request = Receive data from POST request, it gives us access to incoming request
"""
import os
from flask import Flask, jsonify, request, send_from_directory, render_template
from flask_cors import CORS
from wallet import Wallet
from blockchain import Blockchain
from network import Network

LOG_IN_LENGTH = 3

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])  # Decorator
def get_node_ui():
    return send_from_directory('ui', 'node.html')


@app.route('/statistics', methods=['GET'])  # Decorator
def get_statistics_ui():
    return send_from_directory('ui', 'statistics.html')


@app.route('/blockchain', methods=['GET'])  # Decorator
def get_blockchain_ui():
    return send_from_directory('ui', 'blockchain.html')


@app.route('/network', methods=['GET'])  # Decorator
def get_network_ui():
    return send_from_directory('ui', 'network.html')


@app.route('/broadcast-transaction', methods=['POST'])
def broadcast_transaction():
    values = request.get_json()
    if not values:
        response = {'message': 'No data found.'}
        return jsonify(response), 400
    # keys like 'sender' because "values = request.get_json()" returns a dictionary
    required = ['sender', 'recipient', 'amount', 'signature']
    # Checks if all the keys in values accomplish the requirements.
    if not all(key in values for key in required):
        response = {'message': 'Some data is missing.'}
        return jsonify(response), 400
    success = blockchain.add_transaction(values['recipient'], values['sender'], values['signature'], values['amount'], is_receiving=True)
    if success:
        response = {
            'message': 'Successfully added transaction.',
            'transaction': {
                'sender': values['sender'],
                'recipient': values['recipient'],
                'amount': values['amount'],
                'signature': values['signature']
            },
        }
        return jsonify(response), 201
    else:
        response = {
            'message': 'Creating a transaction failed.'
        }
        return jsonify(response), 500


@app.route('/broadcast-block', methods=['POST'])
def broadcast_block():
    values = request.get_json()
    if not values:
        response = {'message': 'No data found.'}
        return jsonify(response), 400
    if 'block' not in values:
        response = {'message': 'Some data is missing'}
        return jsonify(response), 400
    block = values['block']
    if block['index'] == blockchain.chain[-1].index + 1:
        if blockchain.add_block(block):
            response = {'message': 'Block added'}
            return jsonify(response), 201
        else:
            response = {'message': 'Block seems invalid.'}
            print('ERROR:       broadcast_block     Block seems invalid.')
            return jsonify(response), 409
    elif block['index'] > blockchain.chain[-1].index:
        response = {'message': 'Blockchain seems to differ from local blockchain.'}
        blockchain.resolve_conflicts = True
        return jsonify(response), 200
    else:
        response = {'message': 'Blockchain seems to be shorter, block no added'}
        print('ERROR:       broadcast_block     Blockchain seems to be shorter, block no added')
        return jsonify(response), 409


@app.route('/resolve-conflicts', methods=['POST'])
def resolve_conflicts():
    replaced = blockchain.resolve()
    if replaced:
        response = {'message': 'Chain was replaced!'}
    else:
        response = {'message': 'Local chain kept!'}
    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    chain_snapshot = blockchain.chain
    # We have to convert the variable chain_snapshot to dictionary,
    # because json function doesn't works directly with list object.
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
    return jsonify(dict_chain), 200  # HTTP status codes 200=OK [Standard response for successful HTTP requests. ]


@app.route('/node', methods=['POST'])
def add_node():
    values = request.get_json()
    # Values is a dictionary (since get_json() yields one) and hence 'in' check for the existence of keys.
    if 'node' not in values:
        response = {
            'message': 'No node data found.'
        }
        return jsonify(response), 400
    node = values['node']
    if not Network.is_a_valid_ip(node):
        response = {
            'message': 'It is not a valid IP.'
        }
        return jsonify(response), 400
    blockchain.add_peer_node(node)
    response = {
        'message': 'Node added successfully.',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 201


# <node_url> = in the ulr it would replace <node_url> with the value sent it
@app.route('/node/<node_url>', methods=['DELETE'])
def remove_node(node_url):
    if node_url == [] or node_url is None or node_url == '':
        response = {
            'message': 'No node found.'
        }
        return jsonify(response), 400
    blockchain.remove_peer_node(node_url)
    response = {
        'message': 'Node remove',
        'all_nodes': blockchain.get_peer_nodes()
    }
    return jsonify(response), 200


@app.route('/nodes', methods=['GET'])
def get_nodes():
    nodes = blockchain.get_peer_nodes()
    response = {
        'message': 'Nodes loaded.',
        'all_nodes': nodes
    }
    return jsonify(response), 200


@app.route('/userlogin', methods=['POST'])
def user_log_in():
    # Only with the requirement of data must be sent in the json format
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found.'
        }
        return jsonify(response), 400
    required_fields = ['recipient']
    if not all(field in values for field in required_fields):
        response = {
            'message': 'Required data is missing.'
        }
        return jsonify(response), 400
    recipient = values['recipient']
    if len(recipient) != LOG_IN_LENGTH  or recipient.isdigit() is False:
        response = {
            'message': 'ID should be ' + str(LOG_IN_LENGTH) + ' digits long and only numbers!!!'
        }
        return jsonify(response), 400
    global blockchain
    if blockchain.get_users(recipient):
        response = {
            'message': 'The user already voted!'
        }
        return jsonify(response), 400
    response = {
        'message': 'User: ' + recipient + ' has been successfully logged in.',
        'all_user': recipient
    }
    return jsonify(response), 201


@app.route('/userlogout', methods=['GET'])
def user_log_out():
    response = {
        'message': 'Log out successfully.'
    }
    return jsonify(response), 201


@app.route('/vote', methods=['POST'])
def vote():
    values = request.get_json()
    if not values:
        response = {
            'message': 'No data found.',
            'message2': 'Log out successfully.'
        }
        return jsonify(response), 400
    required_fields = ['recipient']
    if not all(field in values for field in required_fields):
        response = {
            'message': 'Required data is missing.',
            'message2': 'Log out successfully.'
        }
        return jsonify(response), 400
    recipient = values['recipient']
    if len(recipient) != LOG_IN_LENGTH or recipient.isdigit() is False:
        response = {
            'message': 'ID should be ' + str(LOG_IN_LENGTH) + ' digits long and only numbers!!!',
            'message2': 'Log out successfully.'
        }
        return jsonify(response), 400
    global blockchain
    if blockchain.get_users(recipient):
        response = {
            'message': 'The user already voted!',
            'message2': 'Log out successfully.'
        }
        return jsonify(response), 400
    # Starting to vote or mine
    wallet.create_keys()
    if not wallet.save_keys():
        response = {
            'message': 'Saving the keys failed.',
            'message2': 'Log out successfully.'
        }
        return jsonify(response), 500
    blockchain = Blockchain(wallet.public_key, port)
    if wallet.public_key is None:
        response = {
            'message': 'No wallet set up.',
            'message2': 'Log out successfully.'
        }
        return jsonify(response), 400
    recipient = values['recipient']
    amount = values['amount']
    signature = wallet.sign_transaction(wallet.public_key, recipient, amount)
    success = blockchain.add_transaction(recipient, wallet.public_key, signature, amount)
    if success:
        if blockchain.resolve_conflicts:
            response = {
                'message': 'Resolve conflicts first, block not added!',
                'message2': 'Log out successfully.'
            }
            return jsonify(response), 409
        block = blockchain.mine_block()
        if block is None:
            response = {
                'message': 'Adding a block failed.',
                'message2': 'Log out successfully.',
            }
            return jsonify(response), 500
        else:
            dict_block = block.__dict__.copy()
            dict_block['transactions'] = [tx.__dict__ for tx in dict_block['transactions']]
            response = {
                'message': 'Vote added successfully.',
                'message2': 'Log out successfully.'
            }
            return jsonify(response), 201
    else:
        response = {
            'message': 'Creating a transaction failed.',
            'message2': 'Log out successfully.'
        }
        return jsonify(response), 500


@app.route('/statistics', methods=['POST'])
def statistics():
    total_votes = blockchain.get_votes()
    if sum(total_votes) == 0:
        response = {
            'message': 'Not data found.'
        }
        return jsonify(response), 400
    response = {
        'message': 'Statistics loaded successfully!',
        'var_votes': total_votes
    }
    return jsonify(response), 201

port = os.getenv('VCAP_APP_PORT', '8000')
if __name__ == '__main__':  # To ensure that I'm running this by directly executing this file.
    # ArgumentParser is a tool that allow us to parse arguments that pass along python file line command
    # For instance, we can run our file like "python3 node.py -p 5000" or "python3 node.py --port 5001"
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=5001)
    args = parser.parse_args()
    port = args.port
    port = int(os.getenv('VCAP_APP_PORT', '8080'))
    wallet = Wallet(port)
    blockchain = Blockchain(wallet.public_key, port)
    app.run(host='0.0.0.0', port=port)
