#NILESH NANDKISHOR AHIRE
#22111065 MSC

import datetime
from requests import request
import hashlib
import json
from flask import Flask, jsonify
from uuid import uuid4
from urllib.parse import urlparse



class Blockchain:
    def __init__(self):  #creating genisis Block
        self.chain = []
        self.transactions = []
        self.create_block (proof = 1, previous_hash='0')
        self.node = set()
       
    def create_block (self, proof, previous_hash): #create new block
        block = {'index': len(self.chain) + 1,
        'timestamp': str(datetime.datetime.now()),
        'proof': proof,
        'previous_hash': previous_hash,
        'transactions':self.transactions}
        self.transactions = []
        self.chain.append(block)
        return block
   
    def get_previous_block(self): #getting previous Block
        return self.chain[-1]
   
    def proof_of_work(self, previous_proof): #
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof+previous_proof).encode()).hexdigest()
            print(hash_operation) #printing hash values (EW CAN SEE ALL HASH VALUES THAT WE TRIED)
            if hash_operation[:2] == '00': #MY MACHINE IS NOT INNUF POWER TO GENERATE '0000' HASH VALUE HENCE IM INCREASING TH ERANGE OF HASH VALUS
                check_proof = True
            else:
                new_proof += 1
        return new_proof
   
    def hash(self, block):
        encoded_block = json.dumps (block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
   
    def is_chain_valid (self, chain):
        block_index=1
        previous_block = chain [0]
        while block_index < len(chain):
            block = chain [block_index]
            if block [ 'previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block ['proof']
            proof = block ['proof']
            hash_operation = hashlib.sha256 (str (proof+previous_proof).encode()).hexdigest()
            if hash_operation [:2] != '00':
                return False
            previous_block = block
            block_index += 1
        return True


    def add_transaction(self,sender,receiver,amount):
        self.transactions.append({'sender':sender,'receiver':receiver,'amount':amount})
        previous_block = self.get_previous_block()
        return previous_block['index'] +1
   
    def add_node(self,address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)
        for node in network:
            response = request.get('http://{node}/get_chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
            if length > max_length and self.is_chain_valid(chain):
                max_length = length
                longest_chain=chain
        if longest_chain:
            self.chain = longest_chain
            return True
        else:
            return False

app=Flask (__name__)
node_address = str(uuid4()).replace('-','')
blockchain=Blockchain()

@app.route("/mine_block", methods = ['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof=blockchain.proof_of_work (previous_proof)
    previous_hash= blockchain.hash (previous_block)
    blockchain.add_transaction(sender= node_address,receiver='Suresh',amount='1')
    block = blockchain.create_block (proof, previous_hash)
    response = { 'message': 'Congratulations!! You have successfully mined a block!',
        'index': block['index'],
        'timestamp':block ['timestamp'],
        'proof':block ['proof'],
        'previous_hash': block ['previous_hash'],
        'transactions' : block['transactions']
        }
    return jsonify (response), 200

@app.route('/get_chain', methods = ['GET'])
def get_chain ():
    response = { 'chain': blockchain.chain,
        'Length': len (blockchain.chain)}
    return jsonify (response), 200

@app.route('/add_transaction',methods = ['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender','receiver','amount']
    if not all (key in json for key in transaction_keys):
        return 'Some elements of the transaction are missing',400
    index = blockchain.add_transaction(json['sender'],json['receiver'],json['amount'])
    response = {'message':f'This transaction will be added to the Block{index}'}
    return jsonify(response),201

@app.route('/connect_node',methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return "No Node",400
    for node in nodes:
        blockchain.add_node(node)
    response = {'message':'All the nodes are now connected. The icoin Blockchain contains the following nodes',
                'total_nodes': list(blockchain.nodes)
                }
    return jsonify(response),201

@app.route('/replace_chain',methods=['GET'])
def replace_chain():
    is_chain_replaced = blockchain.replace_chain()
    if is_chain_replaced:
        response = {'message':'The nodes had different chain so the chain was replaced by the longest chain','new_chain':blockchain.chain}
    else:
        response = {'message':'All good . The chain is the longest one !!','actual_chain': blockchain.chain }
    return jsonify(response),200


@app.route('/is_valid', methods = ['GET'])
def is_valid ():
    is_valid = blockchain.is_chain_valid (blockchain.chain)
    if is_valid:
        response = {'message': 'The Blockchain is valid! '}
    else:
        response = { 'message': 'The Blockchain is not valid! '}
    return jsonify (response), 200


app.run(host = '0.0.0.0', port = 5001)
