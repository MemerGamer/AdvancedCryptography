from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256
import json
import time

class Wallet:
    def __init__(self, owner_name):
        self.owner_name = owner_name
        self.private_key = RSA.generate(2048)
        #self.private_key = RSA.generate(1024) # hogy gyorsabb legyen dolgozhatunk kis kulcsmerettel
        self.public_key = self.private_key.public_key()
        self.balance = 100.0

    def get_address(self):
        # a megfelelo penztarca cim letrehozasa a publikus kulcs alapjan
        public_bytes = self.public_key.export_key('DER')
        return SHA256.new(public_bytes).hexdigest()[:40]

    def sign_transaction(self, transaction_data):
        h = SHA256.new(transaction_data.encode())
        signature = pss.new(self.private_key).sign(h)
        return signature

    def verify_signature(self, data, signature, public_key):
        try:
            verifier = pss.new(public_key)
            h = SHA256.new(data.encode())
            verifier.verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

class Transaction:

    def __init__(self, sender, receiver_address, amount):
        self.sender = sender
        self.receiver_address = receiver_address
        self.amount = amount
        self.timestamp = time.time()
        self.signature = None
        self.transaction_id = None

    def sign(self):
        # a tranzakcio alairasa
        if self.sender.balance < self.amount:
            print(f"Hiba: Tul alacsony egyenleg. {self.sender.owner_name} egyenlege: {self.sender.balance}")
            return False

        transaction_data = self._get_transaction_data()
        self.signature = self.sender.sign_transaction(transaction_data)
        self.transaction_id = self.calculate_hash()
        return True

    def _get_transaction_data(self):
        # a tranzakcio adatainak lekerese, hogy ala lehessen irni
        return json.dumps({
            'sender': self.sender.get_address(),
            'receiver': self.receiver_address,
            'amount': self.amount,
            'timestamp': self.timestamp
        }, sort_keys=True)

    def calculate_hash(self):
        transaction_string = self._get_transaction_data() + (self.signature.hex() if self.signature else "")
        return SHA256.new(transaction_string.encode('utf-8')).hexdigest()

    def is_valid(self):
        # A tranzakcio validalasa
        if self.amount <= 0:
            return False

        if not self.signature:
            return False

        transaction_data = self._get_transaction_data()
        return self.sender.verify_signature(transaction_data, self.signature, self.sender.public_key)

def main():

    alice = Wallet("Alice")
    bob = Wallet("Bob")
    charlie = Wallet("Charlie")

    print(f"\na kovetkezoket hoztuk letre: ")
    print(f"Alice: {alice.get_address()} (Egyenleg: {alice.balance})")
    print(f"Bob: {bob.get_address()} (Egyenleg: {bob.balance})")
    print(f"Charlie: {charlie.get_address()} (Egyenleg: {charlie.balance})")


    tx1 = Transaction(alice, bob.get_address(), 10.0)
    if tx1.sign():
        print("✓ Tranzakcio 1: Alice -> Bob (10 penzegyseg)")
        if tx1.is_valid():
            print("✓ Tranzakcio 1 alairas: ervenyes")
        else:
            print("✗ Tranzakcio 1 alairas: ervenytelen")
    else: print("✗ Tranzakcio 1: nem jott letre")
    print()

    tx2 = Transaction(bob, charlie.get_address(), 150.0)
    if tx2.sign():
        print("✓ Tranzakcio 2: Alice -> Bob (150 penzegyseg)")
        if tx2.is_valid():
            print("✓ Tranzakcio 2 alairas: ervenyes")
        else:
            print("✗ Tranzakcio 2 alairas: ervenytelen")
    else:
        print("✗ Tranzakcio 2: nem jott letre")
    print()

    original_amount = tx1.amount
    original_signature = tx1.signature
    #print(original_amount)
    #print(original_signature)

    print("1. Hamisitasi kiserlet: ")
    tx1.amount = 2000
    if tx1.is_valid():
        print("✓ Tranzakcio 1 alairas: ervenyes")
    else:
        print("✗ Tranzakcio 1: manipulalt")

    print()
    print("2. Hamisitasi kiserlet: ")
    tx1.amount = original_amount
    tx1.signature = original_signature + b'0'
    if tx1.is_valid():
        print("✓ Tranzakcio 1 alairas: ervenyes")
    else:
        print("✗ Tranzakcio 1: manipulalt")

main()