import time
import ast
from hashing import hash
from rsa import generate_keys, sign, verify
class Blockchain:
    def __init__(self):
        self.private_key, self.public_key = generate_keys()
        self.chain = []
        self.current_transactions = []
        self.add_block(timestamp=int(time.time()))

    def load_transactions_from_file(self, filename="transactions.txt"):
        self.current_transactions = []
        with open(filename, "r") as file:
            for line in file:
                transaction = ast.literal_eval(line.strip())
                self.current_transactions.append(transaction)
                self.mine_block()

    def add_block(self, timestamp):
        if len(self.current_transactions) >= 10:
            previous_hash = self.chain[-1].hash if self.chain else '0'
            block_index = len(self.chain) + 1
            new_block = Block(block_index, timestamp, self.current_transactions[:10], previous_hash)
            
            for tx in self.current_transactions[:10]:
                try:
                    Blockchain.verify_transaction(tx)
                except ValueError as e:
                    print(f"Invalid transaction: {e}")
                    return

            if self.validate_block(new_block):
                self.chain.append(new_block)
                self.current_transactions = self.current_transactions[10:]
            else:
                print("Block validation failed")

    def new_transaction(self, sender_private_key, sender_public_key, receiver_public_key, amount):
        transaction = {
            'sender': sender_public_key,
            'receiver': receiver_public_key,
            'amount': amount
        }
        transaction_signature = sign(sender_private_key, str(transaction))
        transaction['signature'] = transaction_signature
        self.current_transactions.append(transaction)
        

    def verify_transaction(transaction):
        sender_public_key = transaction['sender']
        signature = transaction['signature']

        document = {k: transaction[k] for k in transaction if k != 'signature'}
        document_string = str(document)


        if not verify(sender_public_key, document_string, signature):
            raise ValueError("Signature is wrong")
    
        decrypted_signature = ''.join(
            [chr(pow(char, sender_public_key[0], sender_public_key[1])) for char in signature]
        )
        
        if hash(document_string) != decrypted_signature:
            raise ValueError("Document is wrong")

        return True


    def mine_block(self):
        self.add_block(timestamp=int(time.time()))

    def validate_blockchain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].previous_hash != self.chain[i-1].hash:
                return False
        return True
    
    def validate_block(self, new_block):
        if self.chain and new_block.previous_hash != self.chain[-1].hash:
            return False

        return True
    
    def display_blocks(self):
        for block in self.chain:
            print(f"Block Index: {block.index}")
            print(f"Timestamp: {block.timestamp}")
            print(f"Previous Hash: {block.previous_hash}")
            print(f"Current Hash: {block.hash}")
            print(f"Merkle Root: {block.merkle_root}")
            print(f"Transactions Count: {len(block.transactions)}")
            print("-" * 40)



class Block:
    def __init__(self, index, timestamp, transactions, previous_hash='0'):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.merkle_root = self.calculate_merkle_root(transactions)
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f'{self.index}{self.timestamp}{self.merkle_root}{self.previous_hash}'
        return hash(block_string)

    def calculate_merkle_root(self, transactions):
        if not transactions:
            return '0'
        
        transaction_hashes = [hash(str(tx)) for tx in transactions]
        
        while len(transaction_hashes) > 1:
            temp_hashes = []
            for i in range(0, len(transaction_hashes), 2):
                temp_hashes.append(hash(transaction_hashes[i] + (transaction_hashes[i+1] if i+1 < len(transaction_hashes) else transaction_hashes[i])))
            transaction_hashes = temp_hashes
        
        return transaction_hashes[0]