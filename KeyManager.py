import random
import string
import pyaes


class KeyManager:
    def __init__(self):
        letters = string.ascii_lowercase  # lower case string
        # define the condition for random.choice() method
        # random generated key
        self.key = ''.join((random.choice(letters)) for x in range(16))
        # key k' used for encrypting key; known by A and B
        self.k = "cheiedecriptaree"

    def generate_key(self):
        # encrypt key using k
        aes = pyaes.AES(self.k.encode())
        return aes.encrypt(self.key.encode())
