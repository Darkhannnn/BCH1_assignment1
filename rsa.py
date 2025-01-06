import random
from hashing import hash

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    d = 0
    x1, x2, y1 = 0, 1, 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi, e = e, temp2
        x = x2 - temp1 * x1
        y = d - temp1 * y1
        x2, x1 = x1, x
        d, y1 = y1, y
    
    if temp_phi == 1:
        return d + phi

def generate_keys():
    p = random_prime()
    q = random_prime()
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.choice([i for i in range(3, phi) if gcd(i, phi) == 1])
    d = mod_inverse(e, phi)
    return ((e, n), (d, n))

def random_prime():
    primes = [i for i in range(100, 300) if is_prime(i)]
    return random.choice(primes)

def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def encrypt(public_key, message):
    e, n = public_key
    return [pow(ord(char), e, n) for char in message]

def decrypt(private_key, encrypted_message):
    d, n = private_key
    return ''.join([chr(pow(char, d, n)) for char in encrypted_message])



def sign(private_key, document):
    hashed_doc = hash(document)
    return [pow(ord(char), private_key[0], private_key[1]) for char in hashed_doc]

def verify(public_key, document, signature):
    hashed_doc = hash(document)
    decrypted_hash = ''.join([chr(pow(char, public_key[0], public_key[1])) for char in signature])
    return hashed_doc == decrypted_hash
