# Information Security - HW1 - Oprea Ana-Maria B1
Install pyaes library for the AES algortihm.

> pip install pyaes

[ReadMe for pyaes API](https://github.com/ricmoo/pyaes/blob/master/README.md)
```python
#example
import pyaes

# 16 byte block of plain text
plaintext = "Hello World!!!!!"
plaintext_bytes = [ ord(c) for c in plaintext ]

# 32 byte key (256 bit)
key = "This_key_for_demo_purposes_only!"

# Our AES instance
aes = pyaes.AES(key)

# Encrypt!
ciphertext = aes.encrypt(plaintext_bytes)

# [55, 250, 182, 25, 185, 208, 186, 95, 206, 115, 50, 115, 108, 58, 174, 115]
print repr(ciphertext)

# Decrypt!
decrypted = aes.decrypt(ciphertext)

# True
print decrypted == plaintext_bytes
```
