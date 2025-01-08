from blockchain import Blockchain
from wallet import Wallet

blockchain = Blockchain()
blockchain.load_transactions_from_file()
wallet = Wallet()

receiver_wallet = Wallet()
receiver_public_key = receiver_wallet.public_key

for _ in range(20):
    transaction = wallet.create_transaction(receiver_public_key, 9999)
    blockchain.new_transaction(
        sender_private_key=wallet.private_key,
        sender_public_key=wallet.public_key,
        receiver_public_key=receiver_public_key,
        amount=9999
    )
    wallet.save_transaction(transaction)
    blockchain.mine_block()

blockchain.display_blocks()
print("Blockchain valid:", blockchain.validate_blockchain())
