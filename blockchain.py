import time
from hashing import hash

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.add_block(timestamp=int(time.time()))

    def add_block(self, timestamp):
        if len(self.current_transactions) >= 10:
            previous_hash = self.chain[-1].hash if self.chain else '0'
            block_index = len(self.chain) + 1
            new_block = Block(block_index, timestamp, self.current_transactions[:10], previous_hash)
            self.chain.append(new_block)
            self.current_transactions = self.current_transactions[10:]

    def new_transaction(self, sender, receiver, amount):
        self.current_transactions.append({
            'sender': sender,
            'receiver': receiver,
            'amount': amount
        })
        
        if len(self.current_transactions) >= 10:
            self.mine_block()

    def mine_block(self):
        self.add_block(timestamp=int(time.time()))

    def validate_blockchain(self):
        for i in range(1, len(self.chain)):
            if self.chain[i].previous_hash != self.chain[i-1].hash:
                return False
        return True

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

blockchain = Blockchain()

for i in range(20):
    blockchain.new_transaction(f'sender_{i}', f'receiver_{i}', i*10)

for block in blockchain.chain:
    print(f'Block Number: {block.index}')
    print(f'Block Hash: {block.hash}')
    print(f'Previous Hash: {block.previous_hash}')
    print(f'Transactions: {block.transactions}')
    print(f'Merkle Root: {block.merkle_root}')
    print('---')

print(f'Blockchain valid: {blockchain.validate_blockchain()}')
