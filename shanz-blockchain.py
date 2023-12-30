import hashlib
import json
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import random

# Part 1: Digital Identity Creation
def create_wallet():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# Part 2: Blockchain Simulation
class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, public_key):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.public_key = public_key

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], "0", "0", "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def add_block(self, block, signature, public_key):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False

        verifier = pkcs1_15.new(RSA.import_key(public_key))
        try:
            verifier.verify(SHA256.new(block.compute_hash().encode()), signature)
            self.chain.append(block)
            return True
        except (ValueError, TypeError):
            return False

    @property
    def last_block(self):
        return self.chain[-1]

# Part 3: IPFS-like Storage Simulation
class IPFSSimulator:
    def __init__(self):
        self.storage = {}

    def store_data(self, data):
        data_id = str(random.randint(1000, 9999)) # Simple ID generator
        self.storage[data_id] = data
        return data_id

    def retrieve_data(self, data_id):
        return self.storage.get(data_id)

# Demonstration
if __name__ == "__main__":
    # User inputs
    user_name = input("Enter the senior citizen's name: ")

    # Creating wallet for the user
    private_key, public_key = create_wallet()
    print(f"Wallet created for {user_name}. Public Key: {public_key}")

    # Adding a transaction to the blockchain
    blockchain = Blockchain()
    data = {"name": user_name, "health_info": "Sample Health Data"}
    block = Block(1, data, "timestamp_here", blockchain.last_block.hash, public_key.decode())
    
    # Signing the block
    signer = pkcs1_15.new(RSA.import_key(private_key))
    signature = signer.sign(SHA256.new(block.compute_hash().encode()))

    # Adding the block to the blockchain
    success = blockchain.add_block(block, signature, public_key)
    if success:
        print("Transaction added to the blockchain successfully.")
    else:
        print("Failed to add transaction to the blockchain.")

    # Storing additional data using IPFS simulator
    ipfs = IPFSSimulator()
    data_id = ipfs.store_data("Extended Health Data")
    print(f"Data stored in IPFS Simulator with ID: {data_id}")

