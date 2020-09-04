""" ANACONDA: To open anaconda use the command line       $ anaconda-navigator
 ANACONDA: And the in Pycharm you can activate your Environtments, in this case is on terminal:

 $ source activate pycoin

 ANACONDA: Now it will change to (pycoin) at the beginning of the user. For instance, (pycoin) w11@w11: path$
"""
# Initializing our blockchain list

# PYTHON imports
from functools import reduce
# import hashlib as hl
import json
# import pickle
import requests
# MY imports
from utility.hash_util import hash_block
from utility.verification import Verification
from block import Block
from transaction import Transaction
from wallet import Wallet



MINING_REWARD = 10

print(__name__)


class Blockchain:
    def __init__(self, public_key, node_id):
        # Our starting block for the blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Initializing our (empty) blockchian list
        self.__chain = [genesis_block]  # self.__chain = [genesis_block]
        # Unhandled transactions
        self.__open_transactions = []
        self.public_key = public_key
        # sets a network nodes and manages the peer nodes
        self.__peer_nodes = set()
        self.node_id = node_id
        self.resolve_conflicts = False
        self.load_data()  # Read the blockchain.txt file
        #self.load_network()  # Read the network.txt file

    # NEW Generation keys on the node
    # This return the chain attribute into a property with a getter (the method ...
    @property
    def chain(self):
        return self.__chain[:]

    # The setter for the chain property
    @chain.setter
    def chain(self, val):
        self.__chain = val

    def get_chain(self):
        return self.__chain[:]

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open('blockchain-{}.txt'.format(self.node_id), mode='r') as f:
                file_content = f.readlines()
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.__chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                updated_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    updated_transactions.append(updated_transaction)
                self.__open_transactions = updated_transactions
        except (IOError, IndexError):
              print('ERROR:     load_data       Handled exception.')
        finally:
              print('OK:        load_data           Blockchain is loaded!')


    def load_network(self):
        try:
             with open('network-{}.txt'.format(self.node_id), mode='r') as f:
                   file_content = f.readlines()
                   peer_nodes = json.loads(file_content[0])
                   self.__peer_nodes = set(peer_nodes)
        except (IOError, IndexError):
              print('ERROR:     load_network        Handled exception.')
        finally:
              print('OK:        load_network        network file read successful!')


    def save_data(self):
         # Save blocchain + open transaction snapshot to a file
         try:
              with open('blockchain-{}.txt'.format(self.node_id), mode='w') as f:
                   saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in self.__chain]]
                   f.write(json.dumps(saveable_chain))
                   f.write('\n')
                   saveable_tx = [tx.__dict__ for tx in self.__open_transactions]
                   f.write(json.dumps(saveable_tx))
         except IOError:
              print('ERROR:     save_data      Saving blockchain file failed!')


    def save_network(self):
         # Save blocchain + open transaction snapshot to a file
         try:
              with open('network-{}.txt'.format(self.node_id), mode='w') as f:
                   f.write(json.dumps(list(self.__peer_nodes)))
         except IOError:
              print('ERROR:     save_data       Saving network file failed!')


    def proof_of_work(self):
         # Generate a proof of work for the open transactions, the hash of the ...
         last_block = self.__chain[-1]
         last_hash = hash_block(last_block)
         proof = 0
         while not Verification.valid_proof(self.__open_transactions, last_hash, proof):
              proof += 1
         return proof


    def get_balance(self, sender=None):
         # Calculate and return the balance for a participant.
         if sender == None:
              if self.public_key == None:
                   return None
              participant = self.public_key
         else:
              participant = sender
         tx_sender = [[tx.amount for tx in block.transactions if tx.sender == participant] for block in self.__chain]
         open_tx_sender = [tx.amount for tx in self.__open_transactions if tx.sender == participant]
         tx_sender.append(open_tx_sender)
         # reduce comes from functools library
         amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
         tx_recipient = [[tx.amount for tx in block.transactions if tx.recipient == participant] for block in self.__chain]
         amount_receive = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
         return amount_receive - amount_sent


    def get_users(self, recipient=None):
         # Calculate and return the balance for a participant.
         if recipient == None:
                   return None
         else:
              search = recipient
         # rx_recipient return true if the user already voted
         tx_recipient = any([[tx.recipient for tx in block.transactions if tx.recipient == search] for block in self.__chain])
         return tx_recipient


    def get_votes(self):
         tx_votes = [[tx.amount for tx in block.transactions] for block in self.__chain]
         tx_votes2 = [tx_votes.count([1]), tx_votes.count([2]), tx_votes.count([3]), tx_votes.count([4]), tx_votes.count([5]), tx_votes.count([6])]
         return tx_votes2


    def get_last_blockchain_value(self):
         if len(self.__chain) < 1:
              return None
         return self.__chain[-1]


    def add_transaction(self, recipient, sender, signature, amount=0, is_receiving=False):
         """ Arguments:
              :sender: The sender of the coins.
              :recipient: The recipient of the coins.
              :amount: The amount of coins sent with the transaction (default = 1.0)
         """
         # Using the collections library to order the dictionary
         transaction = Transaction(sender, recipient, signature, amount)
         if Verification.verify_transaction(transaction, self.get_balance):
              self.__open_transactions.append(transaction)
              self.save_data()
              if not is_receiving: # Only use this if we are on the node that create the transaction
                   for node in self.__peer_nodes:
                        url = 'http://{}/broadcast-transaction'.format(node)
                        try:
                             response = requests.post(url, json={'sender': sender, 'recipient': recipient, 'amount': amount, 'signature': signature})
                             if response.status_code == 400 or response.status_code == 500:
                                  print('ERROR:     add_transaction         Transaction declined, needs resolving')
                                  return False
                        except requests.exceptions.ConnectionError:
                             continue
              return True
         return False


    def mine_block(self):
         """
             Creates a new block and add block of the blockchain
             Fetch the currently last clock of the blockchain
         """
         # Fetch the currently last block of the blockchain
         if self.public_key == None:
              return None
         last_block = self.__chain[-1]
         hashed_block = hash_block(last_block)
         proof = self.proof_of_work()
         copied_transactions = self.__open_transactions[:]
         for tx in copied_transactions:
             if not Wallet.verify_transaction(tx):
                 return None
         block = Block(len(self.__chain), hashed_block, copied_transactions, proof)
         self.__chain.append(block)
         self.__open_transactions = [] # block mined and transactions are deleted
         self.save_data()
         for node in self.__peer_nodes:
              url = 'http://{}/broadcast-block'.format(node)
              converted_block = block.__dict__.copy()
              converted_block['transactions'] = [tx.__dict__ for tx in converted_block['transactions']]
              try:
                   response = requests.post(url, json={'block': converted_block})
                   if response.status_code == 400 or response.status_code == 500:
                       print('ERROR:        mine_block      Block declined, needs resolving')
                   if response.status_code == 409:
                        self.resolve_conflicts = True
              except requests.exceptions.ConnectionError:
                   continue
         return block


    def add_block(self, block):
         transactions = [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
         proof_is_valid = Verification.valid_proof(transactions[:-1], block['previous_hash'], block['proof'])
         hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
         if not proof_is_valid or not hashes_match:
              print('ERROR:     add_block       proof_is_valid or not hashes_match')
              return False
         converted_block = Block(block['index'], block['previous_hash'], transactions, block['proof'], block['timestamp'])
         self.__chain.append(converted_block)
         stored_transactions = self.__open_transactions[:]
         for itx in block['transactions']:
              for opentx in stored_transactions:
                   if opentx.sender == itx['sender'] and opentx.recipient == itx['recipient'] and opentx.amount == itx['amount'] and opentx.signature == itx['signature']:
                        try:
                             self.__open_transactions.remove(opentx)
                        except ValueError:
                             print('ERROR:      add_block       Item was already removed')
         self.save_data()
         return True


    def resolve(self):
         winner_chain = self.chain
         replace = False
         for node in self.__peer_nodes:
              url = 'http://{}/chain'.format(node)
              try:
                   response = requests.get(url)
                   node_chain = response.json()
                   node_chain = [Block(block['index'], block['previous_hash'], [Transaction(tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']], block['proof'], block['timestamp']) for block in node_chain]
                   node_chain_length = len(node_chain)
                   local_chain_length = len(winner_chain)
                   if node_chain_length > local_chain_length and Verification.verify_chain(node_chain):
                        winner_chain = node_chain
                        replace = True
              except requests.exceptions.ConnectionError:
                   continue
         self.resolve_conflicts = False
         self.chain = winner_chain
         if replace:
              self.__open_transactions = []
         self.save_data()
         return replace


    def add_peer_node(self, node):
         """
         Adds a new node to the peer node set.
          Arguments:
              :node: The node URL which should be added.
         """
         self.__peer_nodes.add(node)
         #  It saves the connect node list to my local blockchain.txt file
         self.save_network()


    def remove_peer_node(self, node):
         """
         Removes a node from the peer node set.

         Arguments:
              :node: The node URL which should be removed.
              :node: The node URL which should be removed.
         """
         self.__peer_nodes.discard(node)
         self.save_network()


    def get_peer_nodes(self):
         """ Return a list of all connected peer nodes."""
         return list(self.__peer_nodes)
