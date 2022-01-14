# Module 1 - creating a Blockchain

import datetime
import hashlib
import json
from flask import Flask, jsonify

# Part 1 - Building a Blockchaingit

class Blockchain:
    def __init__(self):
        self.chain = []
        self.createBlock(proof = 1, previousHash = '0')
        
    def createBlock(self, proof:int, previousHash:str):
        block = {
            'index': len(self.chain)+1,
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previousHash
        }
        
        self.chain.append(block)
        return block
        
    def getPreviousBlock(self):
        return self.chain[-1]
    
    def proofOfWork(self, previousProof: int):
        newProof = 1
        checkProof: bool = False
        
        while checkProof == False:
            hashOperation = hashlib.sha256(str(newProof**2 - previousProof**2).encode()).hexdigest()
            # can't use + because that would make the input symmetrical, and thus ..??
            # using encode to encode the proof expression into SHA256 readable form
            # the digest is returned as a string object of double length, containing only hexadecimal digits
            if hashOperation[:4] == "0000":
                checkProof = True
            else:
                newProof += 1
            
        return newProof
    
    # TO CHECK IF CHAIN IS VALID
    # Checking whether each block has a valid proof of work
    # Checking the prevHash of each block is the hash of the prev block
    
    def hash(self, block: dict):
        encodedBlock: str = json.dumps(block, sort_keys=True).encode() # make dict a string and encode
        return hashlib.sha256(encodedBlock).hexdigest()
    
    def isChainValid(self, chain):
        previousBlock = chain[0]
        blockIndex = 1
        while blockIndex < len(chain):
            # prevhash is same as hash of prev
            thisBlock = chain[blockIndex]
            if thisBlock['previous_hash'] != self.hash(previousBlock):
                return False
            
            # PoW
            previousProof = previousBlock['proof']
            proof = thisBlock['proof']
            hashOperation = hashlib.sha256(str(proof**2 - previousProof**2).encode()).hexdigest()
            if hashOperation[:4] != "0000":
                return False
            
            previousBlock = thisBlock
            blockIndex += 1
        return True
    
# Part 2 - Mining our Blockchain

# creating a web app
app = Flask(__name__)

# creating a Blockchain
blockchain = Blockchain()

# mining a new block
@app.route('/mineBlock', methods = ['GET'])
def mineBlock():
    prevBlock = blockchain.getPreviousBlock()
    prevProof = prevBlock['proof']
    proofOfWork = blockchain.proofOfWork(previousProof=prevProof)
    
    prevHash = blockchain.hash(prevBlock)
    block = blockchain.createBlock(proofOfWork, prevHash)

    response = {'message': "Congratulations, you just mined a block!"}
    for key,val in block.items():
        response[key] = val
        
    return jsonify(response),200

# getting the full blockchain
@app.route('/getChain', methods = ['GET'])
def getChain():
    return jsonify({'chain': blockchain.chain, 
            'length': len(blockchain.chain)
            }), 200

@app.route('/isValid', methods=['GET'])
def isValid():
    return str(blockchain.isChainValid(blockchain.chain))

# running the app
app.run(port = 5000)