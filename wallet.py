from rsa import sign, generate_keys

class Wallet:
    def __init__(self):
        self.private_key, self.public_key = generate_keys()

    def create_transaction(self, receiver_public_key, amount):
        transaction = {
            'sender': self.public_key,
            'receiver': receiver_public_key,
            'amount': amount
        }
        signature = sign(self.private_key, str(transaction))
        transaction['signature'] = signature

        return transaction

    def save_transaction(self, transaction, filename="transactions.txt"):
        with open(filename, "a") as file:
            file.write(str(transaction) + "\n")

    def load_transactions(filename="transactions.txt"):
        transactions = []
        with open(filename, "r") as file:
            for line in file:
                transactions.append(eval(line.strip()))
        return transactions