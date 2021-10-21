import pyaes

encryption = []
decryption = []


class Node:
    def __init__(self):
        # k' key known by A and B and used for encrypting random key
        self.k = "cheiedecriptaree"
        self.op_mode = ""
        self.key = ""
        self.ciphertext = []
        self.message = ""
        # initialization vector - fixed value from the start
        # known by A and B
        self.iv = "InitializationVe"

    def key_decryption(self):
        encoded_key = self.k.encode()
        aes = pyaes.AES(encoded_key)
        # decrypt key using k' encoded and AES algorithm
        self.key = bytes(aes.decrypt(self.key)).decode()

    def get_key(self, key_manager):
        # generate key from key manager
        self.key = key_manager.generate_key()
        # decrypt that key using aes
        self.key_decryption()

    # user input: ecb or ofb
    def input_op_mode(self, key_manager, node):
        self.op_mode = input("[A] choose operation mode (ecb/ofb):")
        while self.op_mode != "ecb" and self.op_mode != "ofb":
            print("wrong command, try again!")
            self.op_mode = input("[A] choose operation mode (ecb/ofb):")
        # set operation mode for B
        node.op_mode = self.op_mode
        # decrypt key for A and B
        self.get_key(key_manager)
        node.get_key(key_manager)
        # B send message (input from keyboard) to A that can start the encryption
        self.start_encryption(node.send_start_message(), node)

    def send_start_message(self):
        self.message = input("[B]type start if you want to start the encryption: ")
        return self.message

    # send encrypted message to B for decryption
    def send_ciphertext(self, ciphertext):
        self.ciphertext = ciphertext

    # B will show the decrypted message, based on operation mode
    def show_decryption(self):
        if self.op_mode == "ecb":
            decrypted_message = self.ecb_decryption(self.ciphertext, self.key)
            print("[B] Decrypted message is:" + decrypted_message)
        elif self.op_mode == "ofb":
            decrypted_message = self.ofb_decryption(self.ciphertext, self.key)
            print("[B] Decrypted message is:" + decrypted_message)

    def start_encryption(self, message, node):
        self.message = message
        if self.message == "start":
            # read message/plaintext from file
            f = open("file.txt", "r")
            plaintext = f.read()
            # check operation mode
            if self.op_mode == "ecb":
                self.ciphertext = self.ecb_encryption(plaintext, self.key)
                # A sends encrypted message to B
                node.send_ciphertext(self.ciphertext)
            elif self.op_mode == "ofb":
                self.ciphertext = self.ofb_encryption(plaintext, self.key)
                # A sends encrypted message to B
                node.send_ciphertext(self.ciphertext)
        else:
            print("you have to type start to encrypt the message")

    # ECB ENCRYPTION
    def aes_encryption(self, block, key):
        if len(block) < 16:  # padding
            for i in range(len(block), 16):
                block += ' '
        aes = pyaes.AES(key.encode())
        return aes.encrypt(block.encode())

    def ecb_encryption(self, plaintext, key):
        # blocks of 128 bits (16 bytes)
        ciphertext = []
        for i in range(0, len(plaintext), 16):
            block = plaintext[i:i + 16]
            ciphertext = ciphertext + self.aes_encryption(block, key)
        return ciphertext

    # OFB ENCRYPTION
    def aes_ofb_encryption(self, block, key, i):
        global encryption
        aes = pyaes.AES(key.encode())
        if i == 0:  # use iv for the first step
            encryption = aes.encrypt(self.iv.encode())
        else:
            # encryption with previous state
            encryption = aes.encrypt(encryption)
        # padding
        if len(block) < 16:
            for i in range(len(block), 16):
                block += ' '
        # block xor encryption
        xor_op = []
        for i in range(0, 16):
            xor_op.append(block.encode()[i] ^ encryption[i])

        return xor_op

    def ofb_encryption(self, plaintext, key):
        # blocks of 128 bits (16 bytes)
        ciphertext = []
        for i in range(0, len(plaintext), 16):
            block = plaintext[i:i + 16]
            ciphertext = ciphertext + self.aes_ofb_encryption(block, key, i)
        return ciphertext

    # ECB DECRYPTION
    def aes_decryption(self, block, key):
        aes = pyaes.AES(key.encode())
        decryption = aes.decrypt(block)
        return bytes(decryption).decode()

    def ecb_decryption(self, ciphertext, key):
        decryption = ""
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i + 16]
            decryption += self.aes_decryption(block, key)
        return decryption

    # OFB DECRYPTION

    def aes_ofc_decryption(self, block, key, i):
        global decryption
        aes = pyaes.AES(key.encode())
        if i == 0:  # use iv for the first step
            decryption = aes.encrypt(self.iv.encode())
        else:
            # decryption with previous state
            decryption = aes.encrypt(decryption)
        # block xor decryption
        xor_op = []
        for i in range(0, 16):
            xor_op.append(block[i] ^ decryption[i])
        return bytes(xor_op).decode()

    def ofb_decryption(self, ciphertext, key):
        decryption = ""
        for i in range(0, len(ciphertext), 16):
            block = ciphertext[i:i + 16]
            decryption += self.aes_ofc_decryption(block, key, i)
        return decryption
